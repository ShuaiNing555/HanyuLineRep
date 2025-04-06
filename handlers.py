from telegram import Update
from telegram.ext import ContextTypes
from data import get_random_word  

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Let's start.")

async def random_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    random_entry = get_random_word()
    await update.message.reply_text(f"Слово: {random_entry['word']}, Перевод: {random_entry['translation']}")