from pathlib import Path

from data.sample_mcq import SAMPLE_MCQ
from generators.reel_generator import generate_reel


def main() -> None:
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "mcq_reel.mp4"
    generate_reel(SAMPLE_MCQ, output_file)
    print(f"Created: {output_file}")


if __name__ == "__main__":
    main()
