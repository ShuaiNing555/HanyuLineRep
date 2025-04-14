FROM python:3.9

WORKDIR /dir3

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]