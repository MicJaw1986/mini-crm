#!/bin/bash
set -e

# Kolory dla outputu
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   MiniCRM Docker Entrypoint${NC}"
echo -e "${GREEN}========================================${NC}"

# Funkcja do czekania na bazę danych
wait_for_db() {
    echo -e "${YELLOW}Czekam na bazę danych...${NC}"

    # Pobierz dane z DATABASE_URL
    if [ -n "$DATABASE_URL" ]; then
        # Ekstrakcja hosta i portu z DATABASE_URL
        # Format: postgresql://user:pass@host:port/dbname
        DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\(.*\):.*/\1/p')
        DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')

        if [ -n "$DB_HOST" ] && [ -n "$DB_PORT" ]; then
            max_attempts=30
            attempt=1

            while [ $attempt -le $max_attempts ]; do
                if pg_isready -h "$DB_HOST" -p "$DB_PORT" > /dev/null 2>&1; then
                    echo -e "${GREEN}Baza danych jest gotowa!${NC}"
                    return 0
                fi
                echo -e "${YELLOW}Próba $attempt/$max_attempts - baza danych nie jest jeszcze gotowa...${NC}"
                sleep 2
                attempt=$((attempt + 1))
            done

            echo -e "${RED}Nie udało się połączyć z bazą danych po $max_attempts próbach${NC}"
            exit 1
        fi
    else
        echo -e "${YELLOW}Używam SQLite, nie trzeba czekać na bazę danych${NC}"
    fi
}

# Funkcja do uruchamiania migracji
run_migrations() {
    echo -e "${YELLOW}Uruchamiam migracje bazy danych...${NC}"
    python manage.py migrate --noinput
    echo -e "${GREEN}Migracje zakończone!${NC}"
}

# Funkcja do zbierania plików statycznych
collect_static() {
    echo -e "${YELLOW}Zbieram pliki statyczne...${NC}"
    python manage.py collectstatic --noinput --clear
    echo -e "${GREEN}Pliki statyczne zebrane!${NC}"
}

# Funkcja do tworzenia superusera (opcjonalnie)
create_superuser() {
    if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ]; then
        echo -e "${YELLOW}Tworzę superusera...${NC}"
        python manage.py createsuperuser --noinput || echo -e "${YELLOW}Superuser już istnieje${NC}"
    fi
}

# Funkcja do uruchamiania crona
start_cron() {
    echo -e "${YELLOW}Uruchamiam cron...${NC}"
    cron
    echo -e "${GREEN}Cron uruchomiony!${NC}"
}

# Główna logika
case "$1" in
    web)
        echo -e "${GREEN}Uruchamiam serwer web...${NC}"
        wait_for_db
        run_migrations
        collect_static
        create_superuser
        start_cron

        # Uruchom serwer (w produkcji używaj gunicorn)
        if [ "$DEBUG" = "True" ]; then
            echo -e "${YELLOW}Tryb deweloperski - używam runserver${NC}"
            exec python manage.py runserver 0.0.0.0:8000
        else
            echo -e "${GREEN}Tryb produkcyjny - używam gunicorn${NC}"
            exec gunicorn mini_crm.wsgi:application \
                --bind 0.0.0.0:8000 \
                --workers 4 \
                --threads 2 \
                --timeout 120 \
                --access-logfile - \
                --error-logfile - \
                --log-level info
        fi
        ;;

    worker)
        echo -e "${GREEN}Uruchamiam worker (tylko cron)...${NC}"
        wait_for_db
        start_cron

        # Trzymaj kontener działającym i wyświetlaj logi crona
        echo -e "${GREEN}Worker uruchomiony. Logi cron:${NC}"
        exec tail -f /var/log/cron.log
        ;;

    migrate)
        echo -e "${GREEN}Uruchamiam tylko migracje...${NC}"
        wait_for_db
        run_migrations
        ;;

    bash|sh)
        echo -e "${GREEN}Uruchamiam shell...${NC}"
        exec /bin/bash
        ;;

    *)
        echo -e "${YELLOW}Uruchamiam komendę: $@${NC}"
        exec "$@"
        ;;
esac
