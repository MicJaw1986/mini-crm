@echo off
REM Skrypt pomocniczy do zarządzania środowiskiem Docker dla MiniCRM (Windows)

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="start" goto start
if "%1"=="stop" goto stop
if "%1"=="restart" goto restart
if "%1"=="build" goto build
if "%1"=="logs" goto logs
if "%1"=="shell" goto shell
if "%1"=="manage" goto manage
if "%1"=="sync" goto sync
if "%1"=="cron-logs" goto cron-logs
if "%1"=="clean" goto clean
goto unknown

:help
echo MiniCRM Docker Manager
echo.
echo Uzycie: docker-dev.bat [komenda]
echo.
echo Dostepne komendy:
echo   start       - Uruchom kontenery
echo   stop        - Zatrzymaj kontenery
echo   restart     - Restartuj kontenery
echo   build       - Przebuduj obrazy
echo   logs        - Pokaz logi
echo   shell       - Wejdz do kontenera (bash)
echo   manage      - Uruchom komende Django (np: docker-dev.bat manage migrate)
echo   sync        - Reczna synchronizacja z ERP
echo   cron-logs   - Pokaz logi synchronizacji (cron)
echo   clean       - Zatrzymaj i usun kontenery + volumes
echo   help        - Pokaz ta pomoc
echo.
goto end

:start
echo Uruchamiam kontenery...
docker-compose up -d
echo Kontenery uruchomione!
docker-compose ps
goto end

:stop
echo Zatrzymuje kontenery...
docker-compose stop
echo Kontenery zatrzymane
goto end

:restart
echo Restartuje kontenery...
docker-compose restart
echo Kontenery zrestartowane
goto end

:build
echo Przebudowuje obrazy...
docker-compose build
echo Obrazy przebudowane
goto end

:logs
docker-compose logs -f
goto end

:shell
echo Wchodze do kontenera web...
docker-compose exec web bash
goto end

:manage
shift
echo Uruchamiam: python manage.py %*
docker-compose exec web python manage.py %*
goto end

:sync
echo Uruchamiam synchronizacje z ERP...
echo 1. Klienci...
docker-compose exec web python manage.py sync_erp_customers
echo 2. Zamowienia...
docker-compose exec web python manage.py sync_erp_orders
echo 3. Faktury...
docker-compose exec web python manage.py sync_erp_invoices
echo Synchronizacja zakonczona!
goto end

:cron-logs
echo Logi synchronizacji (cron):
docker-compose exec web tail -f /var/log/cron.log
goto end

:clean
echo UWAGA: To usunie wszystkie kontenery i dane w volumes!
set /p confirm="Czy na pewno chcesz kontynuowac? (y/N): "
if /i "%confirm%"=="y" (
    docker-compose down -v
    echo Wyczyszczono
) else (
    echo Anulowano
)
goto end

:unknown
echo Nieznana komenda: %1
echo.
goto help

:end
