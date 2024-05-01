FROM python:3.11.9-slim-bullseye

WORKDIR /usr/local/bin

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY validate.py .
COPY score.py .
