# Mini CRM - System Zarządzania Relacjami z Klientami

![Django](https://img.shields.io/badge/Django-5.0-green)
![Python](https://img.shields.io/badge/Python-3.12+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

Webowa aplikacja CRM do zarządzania kontaktami biznesowymi, firmami i interakcjami z klientami. Projekt zaliczeniowy na kurs AI.

## Funkcjonalności

- ✅ **Autentykacja** - rejestracja, logowanie, wylogowanie
- ✅ **Zarządzanie kontaktami** - pełny CRUD, wyszukiwanie, filtrowanie
- ✅ **Zarządzanie firmami** - organizacja kontaktów według firm
- ✅ **Interakcje** - notatki, telefony, emaile, spotkania z timeline
- ✅ **Zadania** - zarządzanie zadaniami z terminami i statusami
- ✅ **Dashboard** - podsumowanie aktywności i statystyki
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
pytest
```

### Testy z pokryciem
```bash
pytest --cov=. --cov-report=html
```

### Testy E2E (Playwright)
```bash
# Instalacja przeglądarek (jednorazowo)
playwright install chromium

# Uruchomienie testów E2E
pytest tests/e2e/
```

## Deployment

### Railway (Zalecane)

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

## Roadmap (Future Features)

- [ ] Eksport kontaktów do CSV
- [ ] Import kontaktów z CSV
- [ ] Powiadomienia email
- [ ] Zaawansowane raporty i wykresy
- [ ] API REST
- [ ] Integracje (Gmail, Google Calendar)
- [ ] Mobile app

---

**Status:** 🚧 W rozwoju

**Wersja:** 1.0.0 (MVP)
