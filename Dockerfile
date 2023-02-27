# Dockerfile
FROM python:3.10-alpine

WORKDIR /telegram-apod-bot

COPY requirements.txt .


RUN pip install -r requirements.txt

COPY .env .
COPY ./bot ./bot

CMD ["python", "./bot/__main__.py"]