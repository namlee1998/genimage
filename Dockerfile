# Stage 1: Build React frontend
FROM node:18 AS frontend-builder
WORKDIR /app/frontend

# Cài dependencies
COPY frontend/package*.json ./
RUN npm ci --no-audit --progress=false || npm install

# Build React
COPY frontend/ ./
RUN npm run build

# Stage 2: Build FastAPI backend
FROM python:3.11-slim AS backend
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Cài Python deps
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend
COPY backend/trainimage.jpg ./backend/trainimage.jpg

# Copy React build output vào backend/build
COPY --from=frontend-builder /app/frontend/build ./backend/build

# Tạo thư mục cần thiết
RUN mkdir -p backend/generated backend/static

EXPOSE 8080
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT}", "--timeout-keep-alive", "120"]
