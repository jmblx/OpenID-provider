FROM python:3.12.7-alpine

RUN apk add --no-cache make build-base ca-certificates && \
    apk add --no-cache --virtual .build-deps gcc musl-dev

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/usr/src

WORKDIR /investments-app

# Копируем сертификаты в контейнер
COPY ./mincifri_certs/russian_trusted_root_ca_pem.crt ./mincifri_certs/russian_trusted_sub_ca_pem.crt /usr/local/share/ca-certificates/russian-trusted/

RUN update-ca-certificates

# Копируем pyproject.toml и устанавливаем зависимости через poetry
COPY pyproject.toml ./
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-dev

COPY . .

RUN chmod +x Makefile