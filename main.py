import asyncio
import nest_asyncio
from telegram.ext import ApplicationBuilder, CommandHandler
from database import init_db
from handlers import start_command, random_word
from db_credentials import BOT_TOKEN

nest_asyncio.apply()

async def main():
    await init_db() 

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("random", random_word))

    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())