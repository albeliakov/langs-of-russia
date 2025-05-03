# Запуск
```bash
# docker-compose pull       # подтянуть обновлённые образы (если используются внешние)
docker-compose up --build -d
```

# Запросить файл БД с удаленной машины
```bash
scp you@remote.host:/var/lib/langs-of-russia/data/app.db .
```