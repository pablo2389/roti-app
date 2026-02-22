FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Install system dependencies (including Pillow build deps)
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

# Copy requirements from backend
COPY backend/requirements.txt* ./
# Upgrade installer tools first (helps build wheels like Pillow)
RUN pip install --upgrade pip setuptools wheel && \
    if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Copy backend code
COPY backend/ ./

# Create static directory for images
RUN mkdir -p app/static/images

# Create non-root user
RUN addgroup --system app && adduser --system --ingroup app app
USER app

EXPOSE 8000

# Run migrations (if DATABASE_URL is set) then start app
CMD ["/bin/bash", "-c", "if [ -n \"$DATABASE_URL\" ]; then alembic upgrade head || true; fi && exec uvicorn app.main:app --host 0.0.0.0 --port $PORT --proxy-headers"]
