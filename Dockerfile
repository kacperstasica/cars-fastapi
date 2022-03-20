FROM python:3.8

RUN pip install pipenv

WORKDIR /app

COPY . /app

RUN pipenv install --system --deploy

EXPOSE 8000
