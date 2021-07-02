FROM python:3.8
MAINTAINER Epifanov Kirill 'xoklhyip@yandex.ru'

RUN apt-get update && apt-get install -y python-pip python-dev build-essential redis

WORKDIR /test_task_backend 

COPY app app
COPY tests tests
COPY requirements.txt test_task_backend.py celery_worker.py config.py pytest.ini app_start.sh ./

RUN chmod 777 *.sh

ENV FLASK_APP test_task_backend.py

RUN pip3 install -r requirements.txt

RUN ./celery_start.sh &

EXPOSE 5000
ENTRYPOINT [ "./app_start.sh" ]
