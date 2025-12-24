# comfy_client.py
import json
import requests
import uuid
import time
from pathlib import Path

COMFY_URL = "http://127.0.0.1:8188"
COMFY_VIDEO_DIR = Path("E:/ComfyUI/ComfyUI/output") #修改为自己的comfyUI输出路径

def generate_video(
    image_path: Path,
    workflow_path: Path,
    width: int,
    height: int,
    length: int,
    batch_size: int,
    prompt: str,
    negative_prompt: str = "",
    timeout: int = 900  # 秒
):
    # 1. 读取 workflow
    print("🔄 读取 workflow:", workflow_path)
    with open(workflow_path, "r", encoding="utf-8") as f:
        workflow = json.load(f)

    # 2. 上传图片到 Comfy
    print("📤 上传图片到 Comfy")
    with open(image_path, "rb") as f:
        r = requests.post(f"{COMFY_URL}/upload/image", files={"image": f})
    r.raise_for_status()
    image_name = r.json()["name"]

    # 3. 绑定图片节点
    workflow["52"]["inputs"]["image"] = image_name

    # 4. 写入参数
    workflow["50"]["inputs"].update({
        "width": width,
        "height": height,
        "length": length,
        "batch_size": batch_size
    })

    # 5. Prompt / Negative Prompt
    workflow["6"]["inputs"]["text"] = prompt
    workflow["7"]["inputs"]["text"] = negative_prompt

    # 6. 提交任务
    print("🧠 提交 Comfy Prompt")
    client_id = str(uuid.uuid4())
    payload = {"prompt": workflow, "client_id": client_id}
    resp = requests.post(f"{COMFY_URL}/prompt", json=payload)
    resp.raise_for_status()
    prompt_id = resp.json()["prompt_id"]
    print(f"🚀 Comfy 任务提交成功: {prompt_id}")

    # 7. 轮询输出目录，等待视频生成（避免拿到旧视频）
    print("⏳ 等待视频生成...")
    start_time = time.time()

    # 记录提交任务前已有的视频文件
    existing_videos = set(COMFY_VIDEO_DIR.glob("*.mp4"))

    while True:
        if time.time() - start_time > timeout:
            raise TimeoutError("视频生成超时")

        all_videos = set(COMFY_VIDEO_DIR.glob("*.mp4"))
        new_videos = all_videos - existing_videos  # 差集就是新生成的视频

        if new_videos:
            latest_video = max(new_videos, key=lambda f: f.stat().st_mtime)
            print("🎬 新视频生成完成:", latest_video)
            return latest_video

        time.sleep(2)
