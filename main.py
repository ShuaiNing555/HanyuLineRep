import os
import logging
from dotenv import load_dotenv
from database import init_db
from handlers import start_command, button_handler, random_word
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

if not BOT_TOKEN or not DATABASE_URL:
    logging.error("ОПроблема с BOT_TOKEN или DATABASE_URL.")
    exit(1)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def main():
    try:
        init_db()  

        application = ApplicationBuilder().token(BOT_TOKEN).build()

        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("random", random_word))
        application.add_handler(CallbackQueryHandler(button_handler))

        logging.info("Бот запущен и готов к работе.")
        application.run_polling() 
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()  