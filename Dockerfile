FROM python:3.8-slim

# set work directory
# WORKDIR /usr/src/app 

# set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app
