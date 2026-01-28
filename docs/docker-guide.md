# MiniCRM - Przewodnik Docker

Ten przewodnik opisuje jak uruchomić MiniCRM w kontenerach Docker z automatyczną synchronizacją ERP przy użyciu crona.

## Architektura

Rozwiązanie składa się z:
- **Kontenera web**: Aplikacja Django + Cron (synchronizacja w tle)
- **Kontenera db**: PostgreSQL (opcjonalnie, można używać SQLite)
- **Crona**: Uruchamia zadania synchronizacji ERP w regularnych odstępach czasu

## Szybki start

### 1. Skopiuj i skonfiguruj zmienne środowiskowe

```bash
cp .env.example .env
```

Edytuj `.env` i wypełnij wymagane wartości:
```bash
# Django
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (dla Docker)
DATABASE_URL=postgresql://minicrm_user:minicrm_password@db:5432/minicrm

# ERP Integration
COMARCH_API_URL=https://twoj-serwer-erp.com/api
COMARCH_API_KEY=your-api-key
ERP_INTEGRATION_ENABLED=True
ERP_CACHE_ENABLED=True

# Superuser
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=secure-password-here
DJANGO_SUPERUSER_EMAIL=admin@yourdomain.com
```

### 2. Zbuduj i uruchom kontenery

```bash
# Zbuduj obrazy
docker-compose build

# Uruchom w tle
docker-compose up -d

# Zobacz logi
docker-compose logs -f
```

### 3. Sprawdź status

```bash
# Status kontenerów
docker-compose ps

# Logi aplikacji
docker-compose logs web

# Logi synchronizacji (cron)
docker-compose exec web tail -f /var/log/cron.log
```

## Konfiguracja harmonogramu synchronizacji

Edytuj plik `docker/crontab` aby dostosować częstotliwość synchronizacji:

```bash
# Synchronizacja klientów - co 6 godzin
0 */6 * * * cd /app && /usr/local/bin/python manage.py sync_erp_customers >> /var/log/cron.log 2>&1

# Synchronizacja zamówień - co 2 godziny
0 */2 * * * cd /app && /usr/local/bin/python manage.py sync_erp_orders >> /var/log/cron.log 2>&1

# Synchronizacja faktur - co 4 godziny
0 */4 * * * cd /app && /usr/local/bin/python manage.py sync_erp_invoices >> /var/log/cron.log 2>&1
```

### Format crontab

```
* * * * * command
│ │ │ │ │
│ │ │ │ └─── dzień tygodnia (0-7, 0 i 7 = niedziela)
│ │ │ └───── miesiąc (1-12)
│ │ └─────── dzień miesiąca (1-31)
│ └───────── godzina (0-23)
└─────────── minuta (0-59)
```

### Przykłady

```bash
*/5 * * * *   # Co 5 minut
0 * * * *     # Co godzinę
0 */6 * * *   # Co 6 godzin
0 2 * * *     # Codziennie o 2:00
0 0 * * 0     # Co tydzień w niedzielę o północy
0 0 1 * *     # Pierwszego dnia miesiąca o północy
```

Po zmianie `docker/crontab`, przebuduj kontener:

```bash
docker-compose build web
docker-compose up -d web
```

## Komendy zarządzania

### Podstawowe operacje

```bash
# Uruchom kontenery
docker-compose up -d

# Zatrzymaj kontenery
docker-compose stop

# Zatrzymaj i usuń kontenery
docker-compose down

# Zatrzymaj i usuń kontenery + volumes (UWAGA: usuwa bazę danych!)
docker-compose down -v

# Przebuduj kontenery po zmianach w kodzie
docker-compose build
docker-compose up -d
```

### Django management commands

```bash
# Migracje
docker-compose exec web python manage.py migrate

# Tworzenie superusera
docker-compose exec web python manage.py createsuperuser

# Shell Django
docker-compose exec web python manage.py shell

# Zbieranie plików statycznych
docker-compose exec web python manage.py collectstatic

# Czyszczenie sesji
docker-compose exec web python manage.py clearsessions
```

### Synchronizacja ERP (manualna)

```bash
# Synchronizuj klientów
docker-compose exec web python manage.py sync_erp_customers

# Synchronizuj zamówienia
docker-compose exec web python manage.py sync_erp_orders

# Synchronizuj faktury
docker-compose exec web python manage.py sync_erp_invoices

# Zobacz status synchronizacji
docker-compose exec web python manage.py sync_status
```

### Logi i monitoring

```bash
# Zobacz wszystkie logi
docker-compose logs

# Zobacz logi konkretnego serwisu
docker-compose logs web
docker-compose logs db

# Śledź logi na żywo
docker-compose logs -f web

# Zobacz logi crona (synchronizacja)
docker-compose exec web tail -f /var/log/cron.log

# Zobacz ostatnie 100 linii logów crona
docker-compose exec web tail -n 100 /var/log/cron.log
```

### Dostęp do kontenerów

```bash
# Bash w kontenerze web
docker-compose exec web bash

# Psql w kontenerze bazy danych
docker-compose exec db psql -U minicrm_user -d minicrm

# Sprawdź procesy crona
docker-compose exec web ps aux | grep cron

# Sprawdź czy cron działa
docker-compose exec web crontab -l
```

## Testowanie harmonogramu crona

Aby przetestować czy cron działa poprawnie bez czekania na zaplanowany czas:

```bash
# 1. Wejdź do kontenera
docker-compose exec web bash

# 2. Ręcznie uruchom komendę synchronizacji
cd /app && python manage.py sync_erp_customers

# 3. Sprawdź logi crona
tail -f /var/log/cron.log
```

Możesz też tymczasowo zmienić harmonogram na częstszy (np. co minutę) do testów:

```bash
# W docker/crontab zmień na:
* * * * * cd /app && /usr/local/bin/python manage.py sync_erp_customers >> /var/log/cron.log 2>&1

# Przebuduj
docker-compose build web
docker-compose up -d web

# Obserwuj logi
docker-compose exec web tail -f /var/log/cron.log
```

## Backup i restore

### Backup bazy danych

```bash
# PostgreSQL
docker-compose exec db pg_dump -U minicrm_user minicrm > backup_$(date +%Y%m%d_%H%M%S).sql

# Lub użyj docker-compose
docker-compose exec -T db pg_dump -U minicrm_user minicrm > backup.sql
```

### Restore bazy danych

```bash
# PostgreSQL
docker-compose exec -T db psql -U minicrm_user minicrm < backup.sql
```

### Backup plików media

```bash
# Skopiuj z kontenera
docker cp minicrm_web:/app/media ./media_backup

# Lub użyj volume
docker run --rm -v minicrm_media_volume:/data -v $(pwd):/backup alpine tar czf /backup/media_backup.tar.gz -C /data .
```

## Produkcja

### Użyj PostgreSQL zamiast SQLite

W `.env`:
```bash
DATABASE_URL=postgresql://minicrm_user:minicrm_password@db:5432/minicrm
```

### Użyj Gunicorn zamiast runserver

W `docker-compose.yml` usługa `web` już używa Gunicorn gdy `DEBUG=False`.

### Dodaj Nginx jako reverse proxy

Odkomentuj sekcję `nginx` w `docker-compose.yml` i utwórz konfigurację:

```nginx
# docker/nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream django {
        server web:8000;
    }

    server {
        listen 80;
        server_name yourdomain.com;

        location /static/ {
            alias /app/staticfiles/;
        }

        location /media/ {
            alias /app/media/;
        }

        location / {
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### Bezpieczeństwo

1. **Zmień domyślne hasła** w `.env`
2. **Użyj silnego SECRET_KEY**
3. **Ustaw DEBUG=False**
4. **Skonfiguruj ALLOWED_HOSTS**
5. **Używaj HTTPS** (Let's Encrypt + Nginx)
6. **Regularnie aktualizuj zależności**

### Monitoring

Rozważ dodanie:
- **Sentry** - monitoring błędów
- **Prometheus + Grafana** - metryki
- **ELK Stack** - centralizacja logów

## Troubleshooting

### Kontener web nie startuje

```bash
# Sprawdź logi
docker-compose logs web

# Sprawdź czy port 8000 jest wolny
netstat -an | grep 8000

# Sprawdź czy baza danych jest dostępna
docker-compose exec web pg_isready -h db -p 5432
```

### Cron nie działa

```bash
# Sprawdź czy cron jest uruchomiony
docker-compose exec web ps aux | grep cron

# Sprawdź crontab
docker-compose exec web crontab -l

# Sprawdź logi crona
docker-compose exec web tail -f /var/log/cron.log

# Sprawdź uprawnienia
docker-compose exec web ls -la /etc/cron.d/django-cron
```

### Błędy synchronizacji ERP

```bash
# Sprawdź konfigurację
docker-compose exec web python manage.py shell
>>> from django.conf import settings
>>> settings.COMARCH_API_URL
>>> settings.ERP_INTEGRATION_ENABLED

# Ręcznie uruchom synchronizację z verbose
docker-compose exec web python manage.py sync_erp_customers -v 2

# Sprawdź logi aplikacji
docker-compose logs web | grep -i erp
```

### Problemy z bazą danych

```bash
# Sprawdź czy PostgreSQL działa
docker-compose ps db

# Sprawdź logi PostgreSQL
docker-compose logs db

# Połącz się z bazą
docker-compose exec db psql -U minicrm_user -d minicrm

# Reset bazy danych (UWAGA: usuwa wszystkie dane!)
docker-compose down -v
docker-compose up -d
```

### Brak plików statycznych (CSS/JS)

```bash
# Zbierz pliki statyczne
docker-compose exec web python manage.py collectstatic --noinput

# Sprawdź czy katalog istnieje
docker-compose exec web ls -la /app/staticfiles
```

## Skalowanie

### Więcej workerów Gunicorn

W `docker/entrypoint.sh` zmień:
```bash
--workers 4  # Zmień na większą liczbę
```

### Osobny kontener dla crona

Jeśli synchronizacja obciąża serwer, utwórz osobny kontener worker:

```yaml
# docker-compose.yml
worker:
  build: .
  command: worker
  volumes:
    - .:/app
  env_file:
    - .env
  depends_on:
    - db
```

## Więcej informacji

- [Docker Documentation](https://docs.docker.com/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [PostgreSQL Docker Guide](https://hub.docker.com/_/postgres)
- [Cron Format](https://crontab.guru/)
