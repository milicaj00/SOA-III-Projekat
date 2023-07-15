
FROM python:3

WORKDIR /usr/app/src

COPY visualization/requirements.txt /
RUN pip install -r /requirements.txt


COPY visualization/app.py ./
COPY visualization/.env ./


CMD [ "python", "app.py"]