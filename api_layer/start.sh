#!/usr/bin/env bash
set -e

# Load .env if present
if [ -f ".env" ]; then
    export $(cat .env | sed 's/#.*//g' | xargs)
fi

exec python -m uvicorn app.main:app \
    --host ${API_HOST:-0.0.0.0} \
    --port ${API_PORT:-8000} \
    --workers 1 \
    --log-level info
