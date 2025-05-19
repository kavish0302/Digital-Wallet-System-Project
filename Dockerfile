FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["sh", "-c", "redis-server --daemonize yes && celery -A wallet_project worker --beat --loglevel=info & python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
