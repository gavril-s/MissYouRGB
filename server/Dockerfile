FROM python:3.11.5-slim-bookworm

ARG port

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.7.1

RUN apt-get -y update; apt-get -y install curl

RUN curl -sSL https://install.python-poetry.org | python3 -

COPY .env /.env
COPY /common /common/

WORKDIR /server
COPY /server/poetry.lock /server/pyproject.toml /server/README.md /server/

RUN poetry install --no-interaction --no-ansi

COPY /server /server/

CMD poetry run python ./server/server.py
EXPOSE $port