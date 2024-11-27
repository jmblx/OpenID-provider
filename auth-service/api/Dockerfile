FROM python:3.12.7-alpine

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH=/usr/src

WORKDIR /fastapi_app

COPY poetry.lock pyproject.toml ./
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

COPY . .

RUN chmod +x /fastapi_app/docker/app.sh
