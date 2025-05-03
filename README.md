# Запуск
Нужно склонировать проект к себе на хост и использовать docker-compose:
```bash
docker-compose up --build -d  # собрать и запустить
docker-compose logs -f web  # логи
docker-compose down # остановить и удалить
```

# Запросить файл БД с удаленной машины
```bash
scp you@remote.host:/var/lib/langs-of-russia/data/app.db .
```