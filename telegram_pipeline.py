from pathlib import Path

from generators.reel_generator import generate_reel
from parsers.telegram_mcq_parser import parse_mcq


def process_telegram_post(text: str, output_name: str = "telegram_mcq_reel.mp4") -> Path:
    """Parse a Telegram MCQ post and generate its Reel."""
    mcq = parse_mcq(text)
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / output_name
    generate_reel(mcq, output_file)
    return output_file


if __name__ == "__main__":
    source = Path("data/sample_telegram_post.txt").read_text(encoding="utf-8")
    print(f"Created: {process_telegram_post(source)}")
