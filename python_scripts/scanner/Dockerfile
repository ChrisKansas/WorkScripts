from python:3-alpine

LABEL maintainer="chris.j.kansas@gmail.com"

COPY . /app
WORKDIR /app

RUN pip install pipenv
RUN pipenv install --system

ENTRYPOINT ["/bin/sh"]
