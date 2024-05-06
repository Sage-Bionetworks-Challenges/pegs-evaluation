FROM ubuntu:22.04

WORKDIR /usr/local/bin

COPY requirements.txt .

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y \
    python3 \
    python3-pip

RUN pip install -r requirements.txt

COPY validate.py .
COPY score.py .
