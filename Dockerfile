# Stage 1 — build dependencies
FROM python:3.12.2-slim AS builder
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2 — final clean image
FROM python:3.12.2-slim
WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /install /usr/local
COPY src/ ./src/
CMD ["python", "src/main.py"]
