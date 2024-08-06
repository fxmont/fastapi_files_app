#!/bin/sh
# chmod +x entrypoint.sh
set -e

# Start cron service
service cron start

# Проверяем статус сервиса cron
sleep 1
STATUS=$(service cron status | grep "running.")

# Проверяем, содержит ли статус строку "running"
if echo "$STATUS" | grep -q "running"; then
    echo "Cron service is active and running."
else
    echo "Cron service is not running or active."
fi

# Apply database migrations
poetry run alembic upgrade head

# Start FastAPI application
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
