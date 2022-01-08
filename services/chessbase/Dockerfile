FROM python:3.8.6-slim-buster

RUN apt-get update
RUN apt-get -y install gcc
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

COPY . /app
WORKDIR /app

RUN adduser --system --home /app --shell /usr/sbin/nologin --no-create-home --disabled-password -u 10000 chessbase

CMD ["./start.sh"]