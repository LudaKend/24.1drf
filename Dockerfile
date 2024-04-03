# используем базовый образ Python версии 3.11 (на его основе будет построен локальный образ)
FROM python:3.11

# устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# копируем файл с зависимостями проекта в рабочую директорию внутри контейнера
COPY ./requirements.txt /app/requirements.txt

# устанавливаем зависимости внутри контейнера
RUN pip install -r /app/requirements.txt

# копируем код приложения(проекта) из текущей папки в рабочую директорию внутри контейнера
COPY . .

# команда для запуска django-приложения из контейнера
#CMD ['python', 'manage.py', 'runserver']