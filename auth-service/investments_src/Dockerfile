FROM ubuntu:22.04

RUN apt update && \
    apt upgrade -y && \
    apt install -y \
    python3 \
    python3-pip \
    ca-certificates \
    openssl \
    build-essential \
    git \
    make

RUN pip3 install --upgrade pip && \
    pip3 install poetry

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/usr/src"

WORKDIR /investments-app

COPY pyproject.toml ./
RUN mkdir /usr/local/share/ca-certificates/russian-trusted
COPY ./mincifri_certs/russian_trusted_root_ca_pem.crt ./mincifri_certs/russian_trusted_sub_ca_pem.crt /usr/local/share/ca-certificates/russian-trusted/

RUN update-ca-certificates

RUN pip3 install --upgrade pip && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-dev

COPY . .

RUN chmod +x Makefile