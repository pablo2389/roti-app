#!/usr/bin/env bash
set -e

# Run migrations then start the app
if [ -n "$DATABASE_URL" ]; then
  echo "Running alembic migrations..."
  alembic upgrade head || true
fi

echo "Starting uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --proxy-headers
