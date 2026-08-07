"""
생활위키 쇼츠 샘플 생성기 (입문용)
- edge-tts 나레이션 + Pillow 카드 + imageio-ffmpeg
사용 예:
  python 미디어/scripts/make_wiki_short.py
필요: pip install edge-tts imageio-ffmpeg pillow
"""
from __future__ import annotations

import asyncio
import os
import re
import subprocess
from pathlib import Path

import edge_tts
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "미디어" / "쇼츠-샘플"
W, H = 1080, 1920

SCRIPT = """VS Code에서 파일 비교, 이렇게 하세요.
지금 연 파일을 기준으로, 명령 팔레트를 엽니다.
Compare Active File With를 실행하세요.
비교할 다른 파일을 고르면, 좌우로 차이가 보입니다.
자세한 내용은 생활위키 VS Code 사용법을 보세요.
"""

SLIDES = [
    "파일 비교\n이렇게 하세요",
    "1. 파일 연 뒤\nCtrl+Shift+P",
    "2. Compare Active\nFile With",
    "3. 다른 파일 선택\n좌우 diff",
    "생활위키에서\n더 보기",
]

VOICE = "ko-KR-SunHiNeural"


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for p in [
        r"C:\Windows\Fonts\malgunbd.ttf",
        r"C:\Windows\Fonts\malgun.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
    ]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def make_slide(text: str, path: Path) -> None:
    img = Image.new("RGB", (W, H), (18, 24, 38))
    draw = ImageDraw.Draw(img)
    draw.text((64, 80), "생활위키", fill=(120, 180, 255), font=font(36))
    ft = font(72)
    lines = text.split("\n")
    sizes = [draw.textbbox((0, 0), ln, font=ft) for ln in lines]
    total_h = sum(s[3] - s[1] for s in sizes) + (len(lines) - 1) * 24
    y = (H - total_h) // 2
    for ln, s in zip(lines, sizes):
        tw = s[2] - s[0]
        x = (W - tw) // 2
        draw.text((x, y), ln, fill=(245, 248, 255), font=ft)
        y += (s[3] - s[1]) + 24
    img.save(path)


async def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    audio = OUT / "narration.mp3"
    await edge_tts.Communicate(SCRIPT.strip(), VOICE).save(str(audio))

    frame_dir = OUT / "frames"
    frame_dir.mkdir(exist_ok=True)
    paths = []
    for i, t in enumerate(SLIDES):
        p = frame_dir / f"slide_{i:02d}.png"
        make_slide(t, p)
        paths.append(p)

    probe = subprocess.run([ffmpeg, "-i", str(audio)], capture_output=True)
    err = probe.stderr.decode("utf-8", errors="replace")
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", err)
    dur = (
        int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
        if m
        else 25.0
    )
    each = max(dur / len(paths), 2.5)

    list_file = OUT / "slides.txt"
    with list_file.open("w", encoding="utf-8") as f:
        for p in paths:
            f.write(f"file '{p.resolve().as_posix()}'\n")
            f.write(f"duration {each:.3f}\n")
        f.write(f"file '{paths[-1].resolve().as_posix()}'\n")

    silent = OUT / "slides.mp4"
    subprocess.check_call(
        [
            ffmpeg,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_file),
            "-vf",
            f"scale={W}:{H},format=yuv420p",
            "-r",
            "30",
            "-pix_fmt",
            "yuv420p",
            str(silent),
        ],
        stderr=subprocess.DEVNULL,
    )

    final = OUT / "wiki-short-vscode-compare.mp4"
    subprocess.check_call(
        [
            ffmpeg,
            "-y",
            "-i",
            str(silent),
            "-i",
            str(audio),
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-shortest",
            "-movflags",
            "+faststart",
            str(final),
        ],
        stderr=subprocess.DEVNULL,
    )
    print(final)


if __name__ == "__main__":
    asyncio.run(main())
