import logging
import os
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters
from telegram_pipeline import process_telegram_post
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger=logging.getLogger(__name__)
BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN")
SOURCE_CHANNEL=os.getenv("TELEGRAM_SOURCE_CHANNEL","").strip()
def channel_matches(update):
    if not SOURCE_CHANNEL: return True
    chat=update.effective_chat
    if not chat: return False
    return (chat.username or "").lower()==SOURCE_CHANNEL.lstrip("@").lower()
async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not channel_matches(update): return
    post=update.channel_post
    if not post or not post.text:
        logger.info("Skipped channel post without text.")
        return
    try:
        output=process_telegram_post(post.text, output_name=f"mcq_{post.message_id}.mp4")
        logger.info("Generated Reel for message %s: %s", post.message_id, output)
    except Exception: logger.exception("Failed to process Telegram message %s", post.message_id)
def main():
    if not BOT_TOKEN: raise RuntimeError("TELEGRAM_BOT_TOKEN is not set.")
    app=Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.UpdateType.CHANNEL_POST, handle_channel_post))
    logger.info("MCQ Telegram listener started.")
    app.run_polling(allowed_updates=["channel_post"])
if __name__=="__main__": main()
