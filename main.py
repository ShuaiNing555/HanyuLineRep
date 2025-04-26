import os
import logging
import asyncio
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
import uvicorn
from fastapi import FastAPI
from api import app as api_app 
from database import init_db
from handlers import start_command, button_handler, random_word
from api import app

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

app = FastAPI()

async def start_fastapi():
    await init_db() 
    uvicorn.run(api_app, host="0.0.0.0", port=8000)

def main():
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_fastapi())

        application = ApplicationBuilder().token(BOT_TOKEN).build()

        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CallbackQueryHandler(button_handler))
        application.add_handler(CommandHandler("random", random_word))

        logging.info("Бот запущен и готов к работе.")
        application.run_polling() 
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
    uvicorn.run(app, host="0.0.0.0", port=8000)