FROM python:3.11

# Создать директорию вашего приложения.
RUN mkdir /app

# Скопировать с локального компьютера файл зависимостей
# в директорию /app.
COPY requirements.txt /app

# Выполнить установку зависимостей внутри контейнера.
RUN pip3 install -r /app/requirements.txt --no-cache-dir

# Скопировать содержимое директории /api_yamdb c локального компьютера
# в директорию /app.
COPY / /app

# Сделать директорию /app рабочей директорией.
WORKDIR /app

# Выполнить запуск сервера разработки при старте контейнера.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8001" ]