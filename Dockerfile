FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "python main.py & celery -A celery_app worker --loglevel=info"]