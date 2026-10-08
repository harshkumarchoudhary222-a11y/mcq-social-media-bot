# MCQ Social Media Bot

Automates exam-MCQ content into social-media-ready graphics and short videos.

## Current pipeline
Telegram-style MCQ text → parser → structured MCQ → 9:16 Reel → MP4

## Telegram parser
The parser accepts common posts containing an exam line, question, four A-D options, an answer, and an optional explanation.

Example:

    Exam: SSC JE Civil
    Q. The purpose of providing weep holes in a retaining wall is to:
    A) Increase the strength of the wall
    B) Relieve the hydrostatic pressure behind the wall
    C) Prevent seepage of rainwater into the wall
    D) Improve the appearance of the wall
    Answer: B
    Explanation: Weep holes allow water behind the wall to drain, reducing hydrostatic pressure.

Run the Telegram-style demo:

    python telegram_pipeline.py

The Reel is written to `output/telegram_mcq_reel.mp4`.

## Local setup
Requirements:
- Python 3.10+
- Pillow
- FFmpeg available on PATH

Install:

    pip install -r requirements.txt

Run the original structured-data demo:

    python main.py

## Next stage
Connect a Telegram Bot API listener to receive new channel posts, pass the post text to `process_telegram_post()`, then add social-platform publishing.

Keep bot tokens and other secrets in environment variables; never commit them to GitHub.