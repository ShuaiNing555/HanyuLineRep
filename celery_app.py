import os
import time
import httpx
from celery import Celery
from dotenv import load_dotenv
import random

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

celery_app = Celery('tasks', broker='sqla+sqlite:///results.db')

@celery_app.task
def send_reminder(chat_id, message):
    time.sleep(5)  
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    print(f"Используемый токен: {BOT_TOKEN}")  
    print(f"Используемый chat_id: {chat_id}")  
    
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    
    try:
        response = httpx.post(url, json=payload)
        response.raise_for_status()  
        print(f"Напоминание отправлено: {message}")
    except httpx.HTTPStatusError as e:
        print(f"Ошибка при отправке напоминания: {e.response.text}")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

send_reminder.apply_async((CHAT_ID, "Ненавязчиво напоминаю, пора работать!"), countdown=10)