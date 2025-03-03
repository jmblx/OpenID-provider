# Используем базовый образ Nginx
FROM nginx:1.21.6

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    libpcre3-dev \
    libssl-dev \
    make \
    zlib1g-dev \
    wget

# Клонируем модуль ngx-http-auth-jwt-module
RUN git clone https://github.com/TeslaGov/ngx-http-auth-jwt-module.git /ngx-http-auth-jwt-module

# Скачиваем исходники Nginx
RUN cd /tmp && \
    wget http://nginx.org/download/nginx-1.21.6.tar.gz && \
    tar -zxvf nginx-1.21.6.tar.gz

# Собираем Nginx с модулем
RUN cd /tmp/nginx-1.21.6 && \
    ./configure --add-module=/ngx-http-auth-jwt-module --with-http_ssl_module && \
    make && make install

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]