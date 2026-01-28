# Mini CRM - System Zarządzania Relacjami z Klientami

![Django CI](https://github.com/TWOJ_USERNAME/MiniCrm/workflows/Django%20CI/badge.svg)
![Django](https://img.shields.io/badge/Django-5.0-green)
![Python](https://img.shields.io/badge/Python-3.12+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen)

Webowa aplikacja CRM do zarządzania kontaktami biznesowymi, firmami i interakcjami z klientami. Projekt zaliczeniowy na kurs AI.

## Funkcjonalności

- ✅ **Autentykacja** - rejestracja, logowanie, wylogowanie
- ✅ **Zarządzanie kontaktami** - pełny CRUD, wyszukiwanie, filtrowanie
- ✅ **Zarządzanie firmami** - organizacja kontaktów według firm
- ✅ **Interakcje** - notatki, telefony, emaile, spotkania z timeline
- ✅ **Zadania** - zarządzanie zadaniami z terminami i statusami
- ✅ **Opportunities** - sales pipeline, zarządzanie szansami sprzedażowymi
- ✅ **Dashboard** - podsumowanie aktywności i statystyki z wykresami
- ⚙️ **Integracja ERP** - podgląd zamówień, faktur, WZ z systemów ERP (Comarch XL, SAP, etc.)
- 🔮 **AI Assistant** - generowanie podsumowań kontaktów (opcjonalne)

## Technologie

- **Backend:** Django 5.x, Python 3.12+
- **Frontend:** Django Templates, Bootstrap 5
- **Database:** SQLite (dev), PostgreSQL (prod)
- **Testing:** pytest, Playwright
- **CI/CD:** GitHub Actions
- **Deployment:** Railway / Render

## Wymagania

- Python 3.12 lub wyższy
- pip
- virtualenv (opcjonalnie)

## Instalacja (Lokalna)

### 1. Klonowanie repozytorium
```bash
git clone https://github.com/TWOJ_USERNAME/mini-crm.git
cd mini-crm
```

### 2. Utworzenie wirtualnego środowiska
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalacja zależności
```bash
pip install -r requirements.txt
```

### 4. Konfiguracja zmiennych środowiskowych
```bash
# Skopiuj przykładowy plik .env
cp .env.example .env

# Edytuj .env i ustaw swoje wartości
# Szczególnie wygeneruj SECRET_KEY
```

Wygeneruj SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Migracje bazy danych
```bash
python manage.py migrate
```

### 6. Utworzenie superużytkownika
```bash
python manage.py createsuperuser
```

### 7. Uruchomienie serwera deweloperskiego
```bash
python manage.py runserver
```

Aplikacja będzie dostępna pod adresem: [http://localhost:8000](http://localhost:8000)

Panel admina: [http://localhost:8000/admin](http://localhost:8000/admin)

## Struktura Projektu

```
mini-crm/
├── docs/                    # Dokumentacja
│   ├── PRD.md
│   ├── tech-spec.md
│   └── user-stories.md
├── mini_crm/                # Projekt Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                # Autentykacja
├── contacts/                # Kontakty i firmy
├── interactions/            # Interakcje
├── tasks/                   # Zadania
├── templates/               # Szablony globalne
├── static/                  # Pliki statyczne
├── tests/                   # Testy
└── manage.py
```

## Uruchamianie Testów

### Testy jednostkowe
```bash
python manage.py test
```

### Testy z pokryciem (coverage)
```bash
# Uruchom testy z pomiarem pokrycia
coverage run --source='.' manage.py test

# Zobacz raport w terminalu
coverage report

# Wygeneruj raport HTML
coverage html
# Otwórz htmlcov/index.html w przeglądarce
```

### Generowanie danych demonstracyjnych
```bash
# Wygeneruj przykładowe dane
python manage.py generate_demo_data

# Wygeneruj dane i wyczyść stare
python manage.py generate_demo_data --clear

# Dane logowania: demo1/demo123, demo2/demo123, demo3/demo123
```

## Deployment

### Docker (Zalecane dla produkcji)

Najprostszy sposób uruchomienia aplikacji z automatyczną synchronizacją ERP.

```bash
# 1. Skopiuj i skonfiguruj zmienne środowiskowe
cp .env.example .env
# Edytuj .env i uzupełnij dane

# 2. Uruchom z Docker Compose
docker-compose up -d

# 3. Aplikacja dostępna na http://localhost:8000
```

Cron automatycznie uruchomi synchronizację z ERP zgodnie z harmonogramem w `docker/crontab`.

**Pełna dokumentacja Docker:** [docs/docker-guide.md](docs/docker-guide.md)

### Railway (Cloud)

1. Załóż konto na [Railway](https://railway.app)
2. Połącz z repozytorium GitHub
3. Railway automatycznie wykryje `Procfile` i `runtime.txt`
4. Ustaw zmienne środowiskowe w panelu Railway:
   - `SECRET_KEY`
   - `DATABASE_URL` (automatycznie z PostgreSQL addon)
   - `ALLOWED_HOSTS`
5. Deploy!

### Render

1. Załóż konto na [Render](https://render.com)
2. Utwórz nową Web Service
3. Połącz z repozytorium
4. Konfiguracja:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn mini_crm.wsgi:application`
5. Dodaj PostgreSQL database
6. Ustaw zmienne środowiskowe
7. Deploy!

## Zmienne Środowiskowe (Produkcja)

```env
SECRET_KEY=<wygenerowany-klucz>
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://user:password@host:5432/dbname
ANTHROPIC_API_KEY=<opcjonalny-klucz-ai>
```

## Licencja

MIT License - zobacz plik LICENSE

## Autor

Projekt zaliczeniowy - Kurs AI

## Linki

- [Dokumentacja Django](https://docs.djangoproject.com/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.3/)
- [Pytest Django](https://pytest-django.readthedocs.io/)
- [Playwright Python](https://playwright.dev/python/)

---

## Integracja z ERP

MiniCRM może integrować się z systemami ERP, wyświetlając dane o zamówieniach, fakturach i dokumentach WZ bezpośrednio w kartach firm.

### Obsługiwane systemy
- ✅ Comarch ERP XL (API REST)
- ⚙️ SAP (w planach)
- ⚙️ Własne API (uniwersalny adapter)

### Quick Start

1. **Skonfiguruj credentials w `.env`:**
```bash
COMARCH_API_URL=https://twoj-serwer-erp.com/api
COMARCH_API_KEY=twoj_api_key
ERP_INTEGRATION_ENABLED=True
```

2. **Wypełnij endpointy API:**
```bash
# Edytuj plik z TODO:
erp_integration/services/comarch_client.py
```

3. **Pełna dokumentacja:**
```bash
erp_integration/README.md        # Kompletny przewodnik
erp_integration/QUICK_START.md   # Tutorial krok po kroku
```

### Funkcje integracji
- 📊 Dane kontrahenta (saldo, limit kredytu, termin płatności)
- 📦 Historia zamówień (status, wartość, daty)
- 📄 Faktury (FS, FKOR, status płatności)
- 📋 Dokumenty WZ
- 💰 Historia płatności
- 📈 Statystyki (nieopłacone faktury, zaległości)

---

## Roadmap (Future Features)

- [ ] Eksport kontaktów do CSV
- [ ] Import kontaktów z CSV
- [ ] Powiadomienia email
- [ ] Zaawansowane raporty i wykresy
- [ ] API REST
- [ ] Integracje (Gmail, Google Calendar)
- [ ] Mobile app
- [ ] Cache ERP data z background sync
- [ ] Webhooks od ERP

---

**Status:** 🚧 W rozwoju

**Wersja:** 1.0.0 (MVP)
