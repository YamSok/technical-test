FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1