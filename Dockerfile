# Dockerfile dla MiniCRM z cronem
FROM python:3.11-slim

# Zmienne środowiskowe
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Katalog roboczy
WORKDIR /app

# Instalacja zależności systemowych
RUN apt-get update && apt-get install -y \
    cron \
    postgresql-client \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Kopiowanie requirements i instalacja pakietów Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Kopiowanie kodu aplikacji
COPY . .

# Kopiowanie i konfiguracja crontab
COPY docker/crontab /etc/cron.d/django-cron
RUN chmod 0644 /etc/cron.d/django-cron && \
    crontab /etc/cron.d/django-cron && \
    touch /var/log/cron.log

# Kopiowanie skryptu entrypoint
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Utworzenie katalogów dla statycznych plików i media
RUN mkdir -p /app/staticfiles /app/media

# Port, na którym działa aplikacja
EXPOSE 8000

# Uruchomienie skryptu entrypoint
ENTRYPOINT ["/entrypoint.sh"]
CMD ["web"]
