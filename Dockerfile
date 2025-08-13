# Stage 1: Build React frontend .
FROM node:18 AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --no-audit --progress=false || npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Build FastAPI backend
FROM python:3.11-slim AS backend
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CHROMA_PATH=/app/data \
    PORT=8080

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

WORKDIR /app
COPY backend/trainimage.jpg /app/backend/trainimage.jpg
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend
COPY --from=frontend-builder /app/frontend/build ./backend/static
RUN mkdir -p /app/data


# Mở cổng 8080 cho Cloud Run
EXPOSE 8080

# Chạy ứng dụng FastAPI bằng uvicorn
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT}"]
