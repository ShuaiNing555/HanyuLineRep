import os
import httpx
from celery import Celery
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

celery_app = Celery('tasks', broker='sqla+sqlite:///results.db')

@celery_app.task(name='send_reminder')
def send_reminder(chat_id, message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
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

celery_app.conf.beat_schedule = {
    'send-reminder-every-30-seconds': {
        'task': 'send_reminder', 
        'schedule': 30.0, 
        'args': (CHAT_ID, "Reminding!"),
    },
}

if __name__ == "__main__":
    celery_app.start()