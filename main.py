import asyncio
import nest_asyncio
from dotenv import load_dotenv
import os
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from database import init_db
from handlers import start_command, button_handler
from data import data_manager


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

nest_asyncio.apply()

async def main():
    await init_db()
    
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(button_handler))

    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())