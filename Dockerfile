# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 5000
CMD  ["gunicorn", "--conf", "app/gunicorn_conf.py", "--bind", "0.0.0.0:5000", "app.api.api:app"]