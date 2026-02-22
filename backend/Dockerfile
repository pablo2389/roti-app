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

# Copy backend requirements and upgrade installer tools
COPY backend/requirements.txt ./requirements.txt
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ ./

# Create static dir for images
RUN mkdir -p app/static/images

# Create non-root user and switch
RUN addgroup --system app && adduser --system --ingroup app app
USER app

EXPOSE 8000

# Run migrations if DATABASE_URL set, then start
CMD ["/bin/bash", "-c", "if [ -n \"$DATABASE_URL\" ]; then alembic upgrade head || true; fi && exec uvicorn app.main:app --host 0.0.0.0 --port $PORT --proxy-headers"]
