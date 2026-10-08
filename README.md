# MCQ Social Media Bot

Automates exam-MCQ content into social-media-ready graphics and short videos.

## Current pipeline
Telegram channel post → parser → structured MCQ → 9:16 Reel → MP4

## Telegram listener
The bot listens for new posts in a Telegram channel where the bot has access. It reads each new text post and sends it through the MCQ parser and Reel generator.

### Setup
1. Create a bot with BotFather and copy its token.
2. Add the bot to the source channel as an administrator.
3. Copy `.env.example` to `.env` and set `TELEGRAM_BOT_TOKEN` and `TELEGRAM_SOURCE_CHANNEL`.
4. Install dependencies with `pip install -r requirements.txt`.
5. Run `python telegram_bot.py`.

Never commit the real bot token to GitHub.

## Source post format
Use an exam line, question, four A-D options, answer, and optional explanation. The parser accepts common A/B/C/D and Answer formats.

    Exam: SSC JE Civil
    Q. The purpose of providing weep holes in a retaining wall is to:
    A) Increase the strength of the wall
    B) Relieve the hydrostatic pressure behind the wall
    C) Prevent seepage of rainwater into the wall
    D) Improve the appearance of the wall
    Answer: B
    Explanation: Weep holes allow water behind the wall to drain, reducing hydrostatic pressure.

## Current limitation
This listener processes **new posts** received while it is running. It does not scrape old channel history.

## Next stage
Add automatic image/carousel generation and publishing to Instagram/Facebook/YouTube.