FROM python:3.11.4-slim-buster

WORKDIR /usr/src/onsiteiq

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt

COPY . .

ENTRYPOINT ["/usr/src/onsiteiq/entry_point.sh"]
