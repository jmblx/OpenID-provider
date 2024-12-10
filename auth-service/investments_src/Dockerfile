FROM python:3.12.7-alpine

# Устанавливаем необходимые пакеты для работы с сертификатами
RUN apk add --no-cache \
    make \
    build-base \
    ca-certificates \
    openssl \
    && apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev

# Копируем сертификаты в нужный каталог
COPY ./mincifri_certs/russian_trusted_root_ca_pem.crt ./mincifri_certs/russian_trusted_sub_ca_pem.crt /usr/local/share/ca-certificates/russian-trusted/

# Обновляем сертификаты в Alpine
RUN update-ca-certificates

# Проверяем, что сертификаты установлены корректно
RUN openssl x509 -in /usr/local/share/ca-certificates/russian-trusted/russian_trusted_root_ca_pem.crt -text -noout

COPY pyproject.toml ./
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-dev

COPY . .

RUN chmod +x Makefile