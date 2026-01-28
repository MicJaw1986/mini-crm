# MiniCRM - Docker Quick Start

Szybkie uruchomienie MiniCRM w kontenerach Docker z automatyczną synchronizacją ERP.

## Wymagania

- Docker Desktop (Windows/Mac) lub Docker Engine (Linux)
- Docker Compose

Sprawdź instalację:
```bash
docker --version
docker-compose --version
```

## 🚀 Uruchomienie w 3 krokach

### 1. Konfiguracja zmiennych środowiskowych

```bash
# Skopiuj przykładowy plik
cp .env.example .env
```

Edytuj `.env` i uzupełnij najważniejsze wartości:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database (automatycznie używa PostgreSQL z docker-compose)
DATABASE_URL=postgresql://minicrm_user:minicrm_password@db:5432/minicrm

# ERP Integration
COMARCH_API_URL=https://twoj-serwer-erp.com/api
COMARCH_API_KEY=twoj-api-key
ERP_INTEGRATION_ENABLED=True
ERP_CACHE_ENABLED=True

# Superuser
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=secure-password
DJANGO_SUPERUSER_EMAIL=admin@example.com
```

### 2. Uruchom kontenery

```bash
# Zbuduj i uruchom
docker-compose up -d

# Zobacz logi
docker-compose logs -f
```

### 3. Otwórz aplikację

🌐 **Aplikacja:** [http://localhost:8000](http://localhost:8000)

🔐 **Login:** admin / secure-password (z Twojego .env)

## ⚙️ Konfiguracja synchronizacji

Harmonogram synchronizacji jest w pliku `docker/crontab`:

```bash
# Synchronizacja klientów - co 6 godzin
0 */6 * * * cd /app && /usr/local/bin/python manage.py sync_erp_customers >> /var/log/cron.log 2>&1

# Synchronizacja zamówień - co 2 godziny
0 */2 * * * cd /app && /usr/local/bin/python manage.py sync_erp_orders >> /var/log/cron.log 2>&1

# Synchronizacja faktur - co 4 godziny
0 */4 * * * cd /app && /usr/local/bin/python manage.py sync_erp_invoices >> /var/log/cron.log 2>&1
```

### Zmiana harmonogramu

1. Edytuj `docker/crontab`
2. Przebuduj kontener:
   ```bash
   docker-compose build web
   docker-compose up -d web
   ```

## 📋 Przydatne komendy

### Zarządzanie kontenerami

```bash
# Uruchom
docker-compose up -d

# Zatrzymaj
docker-compose stop

# Restart
docker-compose restart

# Zobacz status
docker-compose ps

# Zobacz logi
docker-compose logs -f web
```

### Synchronizacja ERP (manualna)

```bash
# Wszystkie dane
./docker-dev.sh sync        # Linux/Mac
docker-dev.bat sync         # Windows

# Lub pojedynczo
docker-compose exec web python manage.py sync_erp_customers
docker-compose exec web python manage.py sync_erp_orders
docker-compose exec web python manage.py sync_erp_invoices
```

### Logi synchronizacji (cron)

```bash
# Linux/Mac
./docker-dev.sh cron-logs

# Windows
docker-dev.bat cron-logs

# Lub bezpośrednio
docker-compose exec web tail -f /var/log/cron.log
```

### Django management commands

```bash
# Migracje
docker-compose exec web python manage.py migrate

# Tworzenie superusera
docker-compose exec web python manage.py createsuperuser

# Shell Django
docker-compose exec web python manage.py shell

# Dane demo
docker-compose exec web python manage.py generate_demo_data
```

### Wejście do kontenera

```bash
# Linux/Mac
./docker-dev.sh shell

# Windows
docker-dev.bat shell

# Lub bezpośrednio
docker-compose exec web bash
```

## 🔍 Weryfikacja działania crona

```bash
# 1. Sprawdź czy cron działa
docker-compose exec web ps aux | grep cron

# 2. Zobacz zaplanowane zadania
docker-compose exec web crontab -l

# 3. Obserwuj logi synchronizacji
docker-compose exec web tail -f /var/log/cron.log

# 4. Test ręczny
docker-compose exec web python manage.py sync_erp_customers
```

## 🛠️ Troubleshooting

### Kontener web nie startuje

```bash
# Zobacz szczegółowe logi
docker-compose logs web

# Sprawdź czy port 8000 jest wolny
netstat -an | grep 8000  # Linux/Mac
netstat -an | findstr 8000  # Windows
```

### Błędy bazy danych

```bash
# Sprawdź czy PostgreSQL działa
docker-compose ps db

# Zobacz logi PostgreSQL
docker-compose logs db

# Połącz się z bazą
docker-compose exec db psql -U minicrm_user -d minicrm
```

### Problemy z synchronizacją

```bash
# Sprawdź czy ERP_INTEGRATION_ENABLED=True w .env
docker-compose exec web python manage.py shell
>>> from django.conf import settings
>>> settings.ERP_INTEGRATION_ENABLED
True

# Ręcznie przetestuj połączenie
docker-compose exec web python manage.py sync_erp_customers -v 2
```

### Cron nie działa

```bash
# Sprawdź czy cron jest uruchomiony
docker-compose exec web service cron status

# Sprawdź uprawnienia crontab
docker-compose exec web ls -la /etc/cron.d/django-cron

# Restart crona
docker-compose restart web
```

### Reset środowiska

```bash
# UWAGA: To usunie wszystkie dane!
docker-compose down -v
docker-compose up -d
```

## 📚 Pełna dokumentacja

Dla bardziej zaawansowanej konfiguracji zobacz:

- **[docs/docker-guide.md](docs/docker-guide.md)** - Kompletny przewodnik Docker
- **[erp_integration/README.md](erp_integration/README.md)** - Integracja z ERP
- **[README.md](README.md)** - Główna dokumentacja projektu

## 💡 Wskazówki

1. **Produkcja**: Zmień `DEBUG=False` i ustaw silny `SECRET_KEY`
2. **HTTPS**: Odkomentuj sekcję nginx w `docker-compose.yml`
3. **Backup**: Regularnie backupuj bazę danych (zobacz docs/docker-guide.md)
4. **Monitoring**: Dodaj Sentry dla logowania błędów
5. **Skalowanie**: Zwiększ liczbę workerów Gunicorn w `docker/entrypoint.sh`

## 🎯 Następne kroki

1. ✅ Uruchom aplikację
2. ✅ Zaloguj się jako admin
3. ✅ Skonfiguruj integrację z ERP w `.env`
4. ✅ Przetestuj ręczną synchronizację
5. ✅ Obserwuj logi crona
6. ✅ Dodaj dane demo: `docker-compose exec web python manage.py generate_demo_data`

---

**Potrzebujesz pomocy?** Sprawdź [docs/docker-guide.md](docs/docker-guide.md) lub otwórz issue na GitHubie.
