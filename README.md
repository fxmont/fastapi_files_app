Перед стартом нужно создать файл src/.env.dev с переменными окружения как в src/env_dev_example

---

### Установить just (опционально)

just (justfile) позволяет быстро запускать команды ([подробнее тут](https://github.com/casey/just?tab=readme-ov-file#packages))

Debian/Ubuntu:
```shell
apt install just
```

## Команды для управления проектом

### Запустить Docker с FastAPI и PostgreSQL
Используя just:
```shell
just up
```

Или командой:
```shell
docker compose -f docker-compose.dev.yml up --build
```

### Остановить Docker контейнеры
Используя just:
```shell
just stop
```

Или командой:
```shell
docker compose -f docker-compose.dev.yml down
```

### Удалить Docker контейнеры и данные
Используя just:
```shell
just erase
```

Или командой:
```shell
docker compose -f docker-compose.dev.yml down -v
```

### Просмотреть логи приложения
Используя just:
```shell
just logs
```

Или командой:
```shell
docker compose -f docker-compose.dev.yml exec fastapi sh -c "cat /app/app.log"
```

### Просмотреть логи приложения в реальном времени
Используя just:
```shell
just logstail
```

Или командой:
```shell
docker compose -f docker-compose.dev.yml exec fastapi sh -c "tail -f /app/app.log"
```

### Создать новую миграцию через Alembic
Используя just:
```shell
just mm "описание миграции"
```

Или командой:
```shell
docker compose -f docker-compose.dev.yml exec fastapi poetry run alembic revision --autogenerate -m "описание миграции"
```

### Применить миграции через Alembic
Используя just:
```shell
just migrate
```

Или командой:
```shell
docker compose -f docker-compose.dev.yml exec fastapi poetry run alembic upgrade head
```

### Откатить миграцию через Alembic
Используя just:
```shell
just downgrade версия
```

Или командой:
```shell
docker compose -f docker-compose.dev.yml exec fastapi poetry run alembic downgrade версия
```

### Посмотреть лог cron (автоматическая очистка папки uploads)
Используя just:
```shell
just cronlog
```

Или командой:
```shell
docker compose -f docker-compose.dev.yml exec fastapi sh -c "cat /var/log/cleanup_uploads.log"
```

### Посмотреть лог cron, последние 10 записей
Используя just:
```shell
just cronlogtail
```

Или командой:
```shell
docker compose -f docker-compose.dev.yml exec fastapi sh -c "tail -f /var/log/cleanup_uploads.log"
```


### Посмотреть содержимое папки uploads в Docker контейнере
Используя just:
```shell
just lsuploads
```

Или командой:
```shell
docker compose -f docker-compose.dev.yml exec fastapi sh -c "ls ./uploads/"
```


### Запуск тестов (pytest)
Сначала запустить Docker контейнер.

Используя just:
```shell
just up
```

Или командой:
```shell
docker compose -f docker-compose.dev.yml up --build
```

Затем запуск тестов:
```shell
pytest
```
