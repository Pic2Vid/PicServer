# main.py
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil

from compose import compose_person_background
from comfy_client import generate_video

app = FastAPI()

# ===== 允许跨域 =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ROOT = Path(__file__).resolve().parent
UPLOAD_DIR = ROOT / "uploads"
OUTPUT_DIR = ROOT / "output"
WORKFLOW_PATH = ROOT / "fusionx_workflow.json"
COMFY_OUTPUT_DIR = Path(r"E:\ComfyUI\ComfyUI\output") #修改为自己的comfyUI输出路径

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

#  静态目录：视频可直接访问
app.mount("/result", StaticFiles(directory=str(OUTPUT_DIR)), name="result")


@app.post("/generate_video/")
async def generate_video_api(
    person: UploadFile,
    background: UploadFile,

    width: int = Form(480),
    height: int = Form(480),
    length: int = Form(25),
    batch_size: int = Form(1),

    prompt: str = Form(...),
    negative_prompt: str = Form("")
):
    # 1. 保存前端上传的图片
    person_path = UPLOAD_DIR / f"person_{person.filename}"
    bg_path = UPLOAD_DIR / f"bg_{background.filename}"

    with open(person_path, "wb") as f:
        shutil.copyfileobj(person.file, f)

    with open(bg_path, "wb") as f:
        shutil.copyfileobj(background.file, f)

    # 2. 抠图 + 合成
    composed_image = OUTPUT_DIR / "output.jpg"
    compose_person_background(person_path, bg_path, composed_image)

    # 3. 调用 ComfyUI
    video_info = generate_video(
        image_path=composed_image,
        workflow_path=WORKFLOW_PATH,
        width=width,
        height=height,
        length=length,
        batch_size=batch_size,
        prompt=prompt,
        negative_prompt=negative_prompt
    )

    filename = video_info.name

    local_video_path = OUTPUT_DIR / filename
    shutil.copy(video_info, local_video_path)

    return {
        "preview_url": f"/result/{filename}",
        "download_url": f"/result/{filename}"
    }


@app.get("/download_video/{filename}")
def download_video(filename: str):
    file_path = OUTPUT_DIR / filename
    return FileResponse(file_path, media_type="video/mp4", filename=filename)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
