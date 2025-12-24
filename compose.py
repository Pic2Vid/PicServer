# compose.py
from rembg import remove
from PIL import Image
from pathlib import Path


def compose_person_background(person_path: Path, background_path: Path, output_path: Path):
    person_img = Image.open(person_path).convert("RGBA")
    person_cut = remove(person_img)

    background = Image.open(background_path).convert("RGBA")

    bg_w, bg_h = background.size
    p_w, p_h = person_cut.size

    scale = (bg_h * 0.7) / p_h
    new_size = (int(p_w * scale), int(p_h * scale))
    person_cut = person_cut.resize(new_size, Image.LANCZOS)

    x = (bg_w - new_size[0]) // 2
    y = bg_h - new_size[1]

    background.paste(person_cut, (x, y), person_cut)
    background.convert("RGB").save(output_path, quality=95)
    print("图片合成成功")

    return output_path
