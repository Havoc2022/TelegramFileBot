from telegram.ext import ApplicationBuilder, MessageHandler, filters
import requests
import os

# -------------------------------
# Environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")       # Your BotFather token
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))  # Your private channel ID
# -------------------------------

# Async handler for documents, photos, videos, audio
async def save_and_link(update, context):
    file = None

    if update.message.document:
        file = update.message.document
    elif update.message.photo:
        file = update.message.photo[-1]  # highest resolution
    elif update.message.video:
        file = update.message.video
    elif update.message.audio:
        file = update.message.audio

    if file:
        # Forward file to your private channel
        await update.message.forward(chat_id=CHANNEL_ID)

        # Get file path from Telegram API
        file_info = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file.file_id}"
        ).json()
        file_path = file_info['result']['file_path']

        # Create direct download link
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

        # Send download link to user
        await update.message.reply_text(
            f"✅ File saved!\n📎 Download link: {file_url}"
        )

# Build and start the bot
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Add handler for all file types
app.add_handler(MessageHandler(
    filters.Document.ALL | filters.PHOTO | filters.VIDEO | filters.AUDIO,
    save_and_link
))

print("Bot is running 24/7...")
app.run_polling()
