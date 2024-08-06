#!/bin/sh

# Директория для очистки
UPLOADS_DIR="/app/uploads"

# Удаляем файлы старше 30 дней
# -exec позволяет выполнить команду для каждого найденного файла.
# rm -f - команда для удаления файлов. Опция -f заставляет rm игнорировать несуществующие файлы и не запрашивать подтверждение перед удалением.
# {} - это место, где find вставляет имя каждого найденного файла.
# \; завершает команду, выполняемую -exec.
# find "$UPLOADS_DIR" -type f -mtime +30 -exec rm -f {} \;

# Удаляем файлы старше 10 секунд
# find "$UPLOADS_DIR" -type f -mmin +0.1 -exec rm -f {} \;

# Удаляем файлы старше 1 минуты
# find "$UPLOADS_DIR" -type f -mmin +1 -exec rm -f {} \;
# echo "Очистка завершена: $(date)"

# Удаляем файлы старше 1 минуты + выводим количество удаленных файлов в лог
COUNT=0
# Поиск и удаление файлов старше 1 минуты
for file in $(find "$UPLOADS_DIR" -type f -mmin +1); do
  rm -f "$file"
  COUNT=$((COUNT + 1))
done

echo "Очистка завершена: $(date). Удалено файлов: $COUNT"
