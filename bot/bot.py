import os
from pathlib import Path
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Load env from project root
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is missing from the .env file.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am Isotope. Ask me anything.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    payload = {
        "message": text,
        "chat_id": str(update.effective_chat.id),
        "user_id": str(update.effective_user.id),
    }

    try:
        response = requests.post("http://localhost:8001/chat", json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        answer = data.get("text", "No response.")
    except Exception:
        answer = "I could not reach the local model bridge."
    await update.message.reply_text(answer)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    print("Isotope bot started...")
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
