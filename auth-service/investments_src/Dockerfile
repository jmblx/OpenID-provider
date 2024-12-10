FROM python:3.12.7-alpine

# Устанавливаем make и другие необходимые инструменты для сборки
RUN apk add --no-cache make build-base

# Настраиваем переменные окружения Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/usr/src

# Устанавливаем рабочую директорию
WORKDIR /investments-app

# Копируем файлы poetry
COPY poetry.lock pyproject.toml ./

# Обновляем pip и устанавливаем Poetry
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

# Копируем код приложения
COPY . .

# Добавляем права на выполнение для Makefile
RUN chmod +x Makefile
