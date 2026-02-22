FROM python:3.11-slim
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Install system dependencies (Pillow build deps + DB client)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    postgresql-client \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    libtiff5-dev \
    libopenjp2-7-dev \
    pkg-config \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user early so we can chown files after copying
RUN addgroup --system app && adduser --system --ingroup app app

# Copy backend requirements and upgrade installer tools
COPY backend/requirements.txt ./requirements.txt
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ ./

# Ensure app directory is writable by non-root user
RUN chown -R app:app /app && mkdir -p /app/app/static/images && chown -R app:app /app/app/static/images

USER app

EXPOSE 8000

# Run migrations if DATABASE_URL set, then start
CMD ["/bin/bash", "-c", "if [ -n \"$DATABASE_URL\" ]; then alembic upgrade head || true; fi && exec uvicorn app.main:app --host 0.0.0.0 --port $PORT --proxy-headers"]
