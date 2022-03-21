FROM python:3.10

RUN pip install pipenv

WORKDIR /app

COPY . /app

RUN pipenv install --system --deploy

EXPOSE 8000
