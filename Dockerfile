# Используем лёгкий образ с Python
FROM python:3.10-slim

# Установка рабочей директории
WORKDIR /app

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем ваш исходный код из папки src/
COPY src/ ./src/

# Создаём папку для файла SQLite
RUN mkdir -p /data

# Переходим в папку с приложением
WORKDIR /app/src

# Открываем порт
EXPOSE 5000

# Запускаем приложение
CMD ["python", "app.py"]
