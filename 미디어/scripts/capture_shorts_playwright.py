"""
Playwright로 웹 화면 캡처 → 쇼츠용 세로 프레임.
데스크톱 VS Code 앱은 제어 불가. vscode.dev / 위키(Pages) / 로컬 HTML 데모 사용.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "미디어" / "쇼츠-샘플"
CAP = OUT / "frames-playwright"
W, H = 1080, 1920
WIKI = "https://jwjhek.github.io/saeng-hwal-wiki/VS-Code-%EC%82%AC%EC%9A%A9%EB%B2%95"
AUDIO = OUT / "narration.mp3"


DIFF_HTML = """<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8"/>
<style>
  html,body{margin:0;height:100%;background:#1e1e1e;color:#ddd;font-family:Consolas,monospace}
  .bar{background:#3c3c3c;padding:10px 16px;font:14px sans-serif}
  .cols{display:flex;height:calc(100% - 40px)}
  .pane{flex:1;padding:16px;overflow:hidden;border-right:1px solid #333}
  .h{color:#888;margin-bottom:12px;font:13px sans-serif}
  .del{background:#5a1d1d;color:#f47171}
  .add{background:#1d5a1d;color:#4ec9b0}
  pre{margin:0;font-size:18px;line-height:1.6}
</style></head><body>
<div class="bar">a.ts ↔ b.ts — Compare Files</div>
<div class="cols">
  <div class="pane"><div class="h">a.ts (활성)</div>
  <pre><span class="del">- const x = 1;</span>
  return x;
}</pre></div>
  <div class="pane"><div class="h">b.ts</div>
  <pre><span class="add">+ const x = 2;</span>
  return x + 1;
}</pre></div>
</div>
</body></html>
"""

PALETTE_HTML = """<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8"/>
<style>
  html,body{margin:0;height:100%;background:#1e1e1e;font-family:Segoe UI,sans-serif;color:#ccc}
  .ed{padding:24px;opacity:.35;font:16px Consolas,monospace;white-space:pre}
  .mask{position:fixed;inset:0;background:rgba(0,0,0,.45)}
  .pal{position:fixed;left:10%;right:10%;top:18%;background:#252526;border-radius:8px;
       box-shadow:0 12px 40px rgba(0,0,0,.5);overflow:hidden}
  .q{padding:14px 18px;background:#3c3c3c;font-size:18px;color:#fff}
  .i{padding:12px 18px;font-size:17px}
  .i.on{background:#094771;color:#fff}
  .hint{position:fixed;left:24px;top:24px;color:#ce9178;font:20px Consolas,monospace}
</style></head><body>
<div class="hint">Ctrl + Shift + P</div>
<div class="ed">function compare() {
  return diff;
}</div>
<div class="mask"></div>
<div class="pal">
  <div class="q">&gt; Compare Active File With</div>
  <div class="i on">Compare Active File With...</div>
  <div class="i">Compare Active File With Saved</div>
  <div class="i">File: Compare Active File With Clipboard</div>
</div>
</body></html>
"""


def font(size: int, bold: bool = False):
    import os

    for p in [
        r"C:\Windows\Fonts\malgunbd.ttf" if bold else r"C:\Windows\Fonts\malgun.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
    ]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def to_vertical(src: Path, dst: Path, caption: str) -> None:
    """웹 캡처를 9:16 캔버스에 넣고 하단 자막."""
    im = Image.open(src).convert("RGB")
    canvas = Image.new("RGB", (W, H), (10, 12, 18))
    draw = ImageDraw.Draw(canvas)
    draw.text((48, 48), "생활위키 · Playwright 캡처", fill=(120, 180, 255), font=font(32, True))

    max_w, max_h = W - 80, H - 280
    ratio = min(max_w / im.width, max_h / im.height)
    nw, nh = int(im.width * ratio), int(im.height * ratio)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    x, y = (W - nw) // 2, 100 + (max_h - nh) // 2
    canvas.paste(im, (x, y))

    bar = (40, H - 170, W - 40, H - 60)
    draw.rounded_rectangle(bar, radius=16, fill=(20, 28, 44))
    f = font(38, True)
    bbox = draw.textbbox((0, 0), caption, font=f)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, H - 140), caption, fill=(245, 248, 255), font=f)
    canvas.save(dst)


def capture() -> list[tuple[Path, str]]:
    CAP.mkdir(parents=True, exist_ok=True)
    shots: list[tuple[Path, str]] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})

        # 1) 위키 문서 (공개 Pages)
        raw1 = CAP / "raw-wiki.png"
        try:
            page.goto(WIKI, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(2500)
            # 비교 섹션으로 스크롤 시도
            page.evaluate(
                """() => {
                const el = [...document.querySelectorAll('h2,h3')].find(e =>
                  (e.textContent||'').includes('파일 비교') ||
                  (e.textContent||'').includes('Compare'));
                if (el) el.scrollIntoView({block:'start'});
            }"""
            )
            page.wait_for_timeout(800)
            page.screenshot(path=str(raw1), full_page=False)
            shots.append((raw1, "위키에 정리된 방법"))
        except Exception as e:
            print("wiki capture skip:", e)

        # 2) vscode.dev — 실제 웹 VS Code
        raw2 = CAP / "raw-vscode.png"
        try:
            page.goto("https://vscode.dev/", wait_until="domcontentloaded", timeout=90000)
            page.wait_for_timeout(5000)
            # 환영/모달 닫기 시도
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)
            page.screenshot(path=str(raw2), full_page=False)
            shots.append((raw2, "vscode.dev 에디터"))
        except Exception as e:
            print("vscode.dev skip:", e)

        # 3) 팔레트 HTML (새 페이지 — vscode.dev TrustedHTML 회피)
        page2 = browser.new_page(viewport={"width": 1280, "height": 800})
        raw3 = CAP / "raw-palette.png"
        page2.set_content(PALETTE_HTML, wait_until="load")
        page2.wait_for_timeout(300)
        page2.screenshot(path=str(raw3), full_page=False)
        shots.append((raw3, "Compare Active File With"))

        # 4) diff HTML
        raw4 = CAP / "raw-diff.png"
        page2.set_content(DIFF_HTML, wait_until="load")
        page2.wait_for_timeout(300)
        page2.screenshot(path=str(raw4), full_page=False)
        shots.append((raw4, "좌우 diff 화면"))

        page2.close()
        browser.close()

    # 세로 프레임
    frames = []
    captions_extra_start = [("파일 비교, 이렇게", None)]  # title card without capture
    # build ordered vertical frames
    out_frames: list[Path] = []
    # title from first wiki or plain
    title = CAP / "v-00.png"
    canvas = Image.new("RGB", (W, H), (18, 24, 38))
    d = ImageDraw.Draw(canvas)
    d.text((48, 56), "생활위키", fill=(120, 180, 255), font=font(34, True))
    d.text((80, 820), "VS Code\n파일 비교", fill=(245, 248, 255), font=font(72, True))
    d.text((80, 1100), "Playwright 캡처 버전", fill=(156, 220, 254), font=font(36))
    canvas.save(title)
    out_frames.append(title)

    for i, (raw, cap) in enumerate(shots, start=1):
        dst = CAP / f"v-{i:02d}.png"
        to_vertical(raw, dst, cap)
        out_frames.append(dst)

    cta = CAP / "v-99.png"
    canvas = Image.new("RGB", (W, H), (18, 24, 38))
    d = ImageDraw.Draw(canvas)
    d.text((48, 56), "생활위키", fill=(120, 180, 255), font=font(34, True))
    d.text((80, 700), "자세한 단계는\n위키에서", fill=(245, 248, 255), font=font(64, True))
    d.text((80, 980), "VS Code 사용법 · 파일 비교", fill=(156, 220, 254), font=font(36))
    canvas.save(cta)
    out_frames.append(cta)
    return out_frames


def mux(frames: list[Path]) -> Path:
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    if not AUDIO.exists():
        raise SystemExit(f"missing audio: {AUDIO}")

    probe = subprocess.run([ffmpeg, "-i", str(AUDIO)], capture_output=True)
    err = probe.stderr.decode("utf-8", errors="replace")
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", err)
    dur = (
        int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
        if m
        else 21.0
    )
    each = max(dur / len(frames), 2.0)

    list_file = OUT / "slides-pw.txt"
    with list_file.open("w", encoding="utf-8") as f:
        for p in frames:
            f.write(f"file '{p.resolve().as_posix()}'\n")
            f.write(f"duration {each:.3f}\n")
        f.write(f"file '{frames[-1].resolve().as_posix()}'\n")

    silent = OUT / "slides-pw.mp4"
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
            str(AUDIO),
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
    return final


if __name__ == "__main__":
    frames = capture()
    final = mux(frames)
    print("frames", len(frames))
    print("DONE", final)
