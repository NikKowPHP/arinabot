FROM python:3.9-slim-buster

WORKDIR /app

COPY ./telegram_bot/requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "telegram_bot/bot.py"]
