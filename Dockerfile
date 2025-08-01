FROM python:3.13.2

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /cw

COPY requirements.txt /cw/requirements.txt

RUN pip install -r /cw/requirements.txt

COPY . .