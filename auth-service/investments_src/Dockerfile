FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    make \
    gcc \
    musl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir poetry

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/usr/src"

WORKDIR /investments-app

COPY pyproject.toml ./
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-dev

COPY . .

RUN mkdir -p /usr/local/share/ca-certificates/russian-trusted && \
    cp ./mincifri_certs/russian_trusted_root_ca_pem.crt /usr/local/share/ca-certificates/russian-trusted/russian_trusted_root_ca.crt && \
    cp ./mincifri_certs/russian_trusted_sub_ca_pem.crt /usr/local/share/ca-certificates/russian-trusted/russian_trusted_sub_ca.crt

RUN update-ca-certificates

RUN chmod +x Makefile
