from __future__ import annotations

import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT, FPS, DURATION = 1080, 1920, 30, 12
YELLOW = (255, 210, 20)
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
GREY = (244, 244, 244)
DARK_GREY = (75, 75, 75)
BORDER = (225, 225, 225)


def _font_path(bold: bool) -> str:
    candidates = (
        [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
        ]
        if bold
        else [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        ]
    )
    for path in candidates:
        if Path(path).exists():
            return path
    raise FileNotFoundError("No suitable system font was found.")


def _font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(_font_path(bold), size)


def _wrap(draw: ImageDraw.ImageDraw, text: str, fnt, max_width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textbbox((0, 0), trial, font=fnt)[2] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def _render_frame(data: dict, time_s: float, path: Path) -> None:
    img = Image.new("RGB", (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(img)

    draw.rectangle((0, 0, WIDTH, 150), fill=YELLOW)
    draw.text((55, 32), "CIVIL ENGINEERING MCQ", font=_font(58), fill=BLACK)
    draw.text((55, 104), data["exam"], font=_font(28, False), fill=BLACK)

    if time_s < 2:
        draw.text((70, 330), "CAN YOU", font=_font(96), fill=BLACK)
        draw.text((70, 450), "SOLVE THIS?", font=_font(96), fill=BLACK)
        draw.text((70, 610), "You have 5 seconds", font=_font(45, False), fill=DARK_GREY)
        draw.rounded_rectangle((70, 760, 1010, 920), radius=35, fill=BLACK)
        draw.text((WIDTH // 2, 840), "TEST YOUR CIVIL ENGINEERING",
                  font=_font(38), fill=WHITE, anchor="mm")

    elif time_s < 7:
        _rounded(draw, (55, 215, 1025, 760), 40, GREY)
        draw.text((90, 250), "Q.1", font=_font(48), fill=BLACK)
        qfont = _font(48)
        y = 340
        for line in _wrap(draw, data["question"], qfont, 840):
            draw.text((90, y), line, font=qfont, fill=BLACK)
            y += 65

        start_y = 790
        option_font = _font(34, False)
        for index, option in enumerate(data["options"]):
            y1 = start_y + index * 210
            _rounded(draw, (55, y1, 1025, y1 + 170), 30, WHITE,
                     outline=BORDER, width=3)
            draw.ellipse((80, y1 + 35, 160, y1 + 115), fill=YELLOW)
            draw.text((120, y1 + 75), chr(65 + index), font=_font(38),
                      fill=BLACK, anchor="mm")
            oy = y1 + 38
            for line in _wrap(draw, option, option_font, 820)[:2]:
                draw.text((190, oy), line, font=option_font, fill=BLACK)
                oy += 48

    elif time_s < 9:
        draw.text((WIDTH // 2, 330), "TIME'S UP!", font=_font(88),
                  fill=BLACK, anchor="mm")
        remaining = max(0, math.ceil(9 - time_s))
        draw.ellipse((270, 500, 810, 1040), fill=YELLOW, outline=BLACK, width=8)
        draw.text((WIDTH // 2, 770), str(remaining), font=_font(210),
                  fill=BLACK, anchor="mm")
        draw.text((WIDTH // 2, 1130), "Did you choose correctly?",
                  font=_font(45, False), fill=DARK_GREY, anchor="mm")

    else:
        draw.text((70, 260), "ANSWER", font=_font(70), fill=BLACK)
        _rounded(draw, (55, 390, 1025, 760), 40, YELLOW)
        draw.text((100, 455), data["answer_label"], font=_font(100), fill=BLACK)
        answer_font = _font(45)
        y = 465
        for line in _wrap(draw, data["options"][data["answer_index"]], answer_font, 780):
            draw.text((220, y), line, font=answer_font, fill=BLACK)
            y += 62

        _rounded(draw, (55, 850, 1025, 1240), 40, GREY)
        draw.text((90, 900), "WHY?", font=_font(48), fill=BLACK)
        why_font = _font(38, False)
        y = 980
        for line in _wrap(draw, data["explanation"], why_font, 860):
            draw.text((90, y), line, font=why_font, fill=BLACK)
            y += 55

        draw.rectangle((0, 1680, WIDTH, HEIGHT), fill=YELLOW)
        draw.text((WIDTH // 2, 1740), "PRACTICE DAILY. CRACK YOUR EXAMS.",
                  font=_font(42), fill=BLACK, anchor="mm")
        draw.text((WIDTH // 2, 1815), data["cta"], font=_font(34, False),
                  fill=BLACK, anchor="mm")

    img.save(path, quality=95)


def generate_reel(data: dict, output_file: Path) -> None:
    frames_dir = output_file.parent / f"{output_file.stem}_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    for frame_index in range(FPS * DURATION):
        frame_path = frames_dir / f"frame_{frame_index:04d}.png"
        _render_frame(data, frame_index / FPS, frame_path)

    command = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(frames_dir / "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-vf", f"scale={WIDTH}:{HEIGHT}",
        "-movflags", "+faststart",
        str(output_file),
    ]

    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, text=True)
    except FileNotFoundError as exc:
        raise RuntimeError(
            "FFmpeg is not installed or not available on PATH."
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"FFmpeg failed: {exc.stderr}") from exc
