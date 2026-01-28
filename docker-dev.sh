#!/bin/bash
# Skrypt pomocniczy do zarządzania środowiskiem Docker dla MiniCRM

set -e

# Kolory
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_help() {
    echo "MiniCRM Docker Manager"
    echo ""
    echo "Użycie: ./docker-dev.sh [komenda]"
    echo ""
    echo "Dostępne komendy:"
    echo "  start       - Uruchom kontenery"
    echo "  stop        - Zatrzymaj kontenery"
    echo "  restart     - Restartuj kontenery"
    echo "  build       - Przebuduj obrazy"
    echo "  logs        - Pokaż logi"
    echo "  shell       - Wejdź do kontenera (bash)"
    echo "  manage      - Uruchom komendę Django (np: ./docker-dev.sh manage migrate)"
    echo "  sync        - Ręczna synchronizacja z ERP"
    echo "  cron-logs   - Pokaż logi synchronizacji (cron)"
    echo "  clean       - Zatrzymaj i usuń kontenery + volumes"
    echo "  help        - Pokaż tę pomoc"
    echo ""
}

case "$1" in
    start)
        echo -e "${GREEN}Uruchamiam kontenery...${NC}"
        docker-compose up -d
        echo -e "${GREEN}Kontenery uruchomione!${NC}"
        docker-compose ps
        ;;

    stop)
        echo -e "${YELLOW}Zatrzymuję kontenery...${NC}"
        docker-compose stop
        echo -e "${GREEN}Kontenery zatrzymane${NC}"
        ;;

    restart)
        echo -e "${YELLOW}Restartuję kontenery...${NC}"
        docker-compose restart
        echo -e "${GREEN}Kontenery zrestartowane${NC}"
        ;;

    build)
        echo -e "${YELLOW}Przebudowuję obrazy...${NC}"
        docker-compose build
        echo -e "${GREEN}Obrazy przebudowane${NC}"
        ;;

    logs)
        docker-compose logs -f
        ;;

    shell)
        echo -e "${GREEN}Wchodzę do kontenera web...${NC}"
        docker-compose exec web bash
        ;;

    manage)
        shift
        echo -e "${GREEN}Uruchamiam: python manage.py $@${NC}"
        docker-compose exec web python manage.py "$@"
        ;;

    sync)
        echo -e "${GREEN}Uruchamiam synchronizację z ERP...${NC}"
        echo -e "${YELLOW}1. Klienci...${NC}"
        docker-compose exec web python manage.py sync_erp_customers
        echo -e "${YELLOW}2. Zamówienia...${NC}"
        docker-compose exec web python manage.py sync_erp_orders
        echo -e "${YELLOW}3. Faktury...${NC}"
        docker-compose exec web python manage.py sync_erp_invoices
        echo -e "${GREEN}Synchronizacja zakończona!${NC}"
        ;;

    cron-logs)
        echo -e "${GREEN}Logi synchronizacji (cron):${NC}"
        docker-compose exec web tail -f /var/log/cron.log
        ;;

    clean)
        echo -e "${RED}UWAGA: To usunie wszystkie kontenery i dane w volumes!${NC}"
        read -p "Czy na pewno chcesz kontynuować? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker-compose down -v
            echo -e "${GREEN}Wyczyszczono${NC}"
        else
            echo -e "${YELLOW}Anulowano${NC}"
        fi
        ;;

    help|"")
        print_help
        ;;

    *)
        echo -e "${RED}Nieznana komenda: $1${NC}"
        echo ""
        print_help
        exit 1
        ;;
esac
