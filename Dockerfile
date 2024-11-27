# Dockerfile
FROM python:3.10-slim

# Cài đặt các thư viện hệ thống cần thiết (nếu có)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y poppler-utils
# Copy file requirements.txt vào container
COPY requirements.txt /app/requirements.txt

# Cài đặt các thư viện từ requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy mã nguồn vào container
COPY . /app

WORKDIR /app
