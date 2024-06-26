FROM python:3.10-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  && apt-get install -y gettext \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # for PostgreSQL
  && apt-get install -y libpq-dev libssl-dev \
  # netcat is used to wait for PostgreSQL to be available
  && apt-get install -y netcat

  
# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app

RUN chmod +x /app/start.sh

WORKDIR /app
