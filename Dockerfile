FROM python:3.12-slim
LABEL authors="Alina"

WORKDIR /app

# Установим системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends git

COPY requirements.txt ./

# Установим зависимости Python
RUN pip install -r requirements.txt

# Скопируем остальное приложение
COPY . .

EXPOSE 5000

CMD ["python", "./app.py"]
