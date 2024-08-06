default:
  just --list

up *args:
  docker compose -f docker-compose.dev.yml up --build {{args}}

stop *args:
  docker compose -f docker-compose.dev.yml down {{args}}

erase *args:
  docker compose -f docker-compose.dev.yml down -v {{args}}

logs:
  docker compose -f docker-compose.dev.yml exec fastapi sh -c "cat /app/app.log"

logstail:
  docker compose -f docker-compose.dev.yml exec fastapi sh -c "tail -f /app/app.log"

mm *args:
  docker compose -f docker-compose.dev.yml exec fastapi poetry run alembic revision --autogenerate -m "{{args}}"

migrate:
  docker compose -f docker-compose.dev.yml exec fastapi poetry run alembic upgrade head

downgrade *args:
  docker compose -f docker-compose.dev.yml exec fastapi poetry run alembic downgrade {{args}}

cronlog:
    docker compose -f docker-compose.dev.yml exec fastapi sh -c "cat /var/log/cleanup_uploads.log"

cronlogtail:
    docker compose -f docker-compose.dev.yml exec fastapi sh -c "tail -f /var/log/cleanup_uploads.log"

lsuploads:
    docker compose -f docker-compose.dev.yml exec fastapi sh -c "ls ./uploads/"
