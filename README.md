# MCQ Social Media Bot

Automates exam-MCQ content into social-media-ready graphics and short videos.

## Phase 1
- Generate a 9:16 MCQ Reel from structured question data.
- Keep rendering deterministic with Pillow + FFmpeg.
- Later phases will add Telegram ingestion, captions, images, and publishing integrations.

## Local setup
Requirements:
- Python 3.10+
- Pillow
- FFmpeg available on PATH

Install:
```bash
pip install -r requirements.txt
```

Run:
```bash
python main.py
```

Output: `output/mcq_reel.mp4`
