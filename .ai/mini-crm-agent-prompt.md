# PROMPT DLA AGENTA AI - Projekt Mini CRM

## KONTEKST PROJEKTU

Jesteś doświadczonym programistą Python/Django, który pomaga mi stworzyć projekt zaliczeniowy na kurs AI. Projekt musi spełniać określone wymagania i być rozwijany iteracyjnie z regularnymi commitami do GitHub.

---

## WYMAGANIA ZALICZENIOWE

### ❗ OBOWIĄZKOWE:
1. **Mechanizm kontroli dostępu** - ekran logowania, rejestracja, wylogowanie
2. **Zarządzanie danymi CRUD** - tworzenie, odczytywanie, aktualizacja, usuwanie elementów
3. **Logika biznesowa** - z integracją AI lub bez
4. **Dokumentacja** - PRD i dokumenty kontekstowe
5. **Testy** - minimum jeden test E2E z perspektywy użytkownika
6. **Pipeline CI/CD** - budowanie aplikacji i uruchamianie testów

### ⭐ OPCJONALNE (na wyróżnienie):
- Projekt dostępny pod publicznym URL

---

## STOS TECHNOLOGICZNY

- **Backend:** Django 5.x
- **Baza danych:** SQLite (development), PostgreSQL (production)
- **Frontend:** Django Templates / Jinja2
- **CSS:** Tailwind CSS (via CDN) lub Bootstrap 5
- **Testy:** pytest + pytest-django + Playwright (E2E)
- **CI/CD:** GitHub Actions
- **Hosting:** Railway / Render / Fly.io
- **AI:** Claude API (Anthropic) lub OpenAI API

---

## OPIS PROJEKTU: MINI CRM

### Cel aplikacji
System do zarządzania kontaktami biznesowymi, firmami i interakcjami z klientami. Zawiera funkcję AI do generowania podsumowań i sugestii następnych kroków.

### Główne funkcjonalności

#### 1. Moduł Użytkowników (accounts)
- Rejestracja nowego użytkownika
- Logowanie / wylogowanie
- Profil użytkownika
- Reset hasła (opcjonalnie)

#### 2. Moduł Kontaktów (contacts)
- Lista kontaktów z wyszukiwaniem i filtrowaniem
- Dodawanie nowego kontaktu
- Edycja kontaktu
- Usuwanie kontaktu
- Przypisanie kontaktu do firmy
- Status kontaktu (lead, prospect, customer, churned)

#### 3. Moduł Firm (companies)
- Lista firm
- CRUD dla firm
- Powiązanie z kontaktami

#### 4. Moduł Interakcji (interactions)
- Notatki do kontaktów
- Historia interakcji (telefon, email, spotkanie)
- Timeline aktywności

#### 5. Moduł Zadań (tasks)
- Zadania przypisane do kontaktów
- Terminy wykonania
- Status zadania (todo, in_progress, done)
- Lista zadań na dziś

#### 6. Moduł AI (ai_assistant)
- Generowanie podsumowania kontaktu na podstawie notatek
- Sugestia następnego kroku
- Analiza sentymentu interakcji (opcjonalnie)

---

## STRUKTURA PROJEKTU

```
mini-crm/
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   ├── PRD.md
│   ├── tech-spec.md
│   └── user-stories.md
├── mini_crm/                    # Główny katalog projektu Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/                    # Aplikacja użytkowników
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│       └── accounts/
│           ├── login.html
│           ├── register.html
│           └── profile.html
├── contacts/                    # Aplikacja kontaktów
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│       └── contacts/
│           ├── contact_list.html
│           ├── contact_detail.html
│           ├── contact_form.html
│           ├── company_list.html
│           ├── company_detail.html
│           └── company_form.html
├── interactions/                # Aplikacja interakcji
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│       └── interactions/
│           └── note_form.html
├── tasks/                       # Aplikacja zadań
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│       └── tasks/
│           ├── task_list.html
│           └── task_form.html
├── ai_assistant/                # Aplikacja AI
│   ├── __init__.py
│   ├── apps.py
│   ├── services.py
│   └── views.py
├── templates/                   # Globalne szablony
│   ├── base.html
│   ├── navbar.html
│   └── dashboard.html
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── main.js
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_accounts.py
│   ├── test_contacts.py
│   ├── test_tasks.py
│   └── e2e/
│       └── test_user_journey.py
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── Procfile
├── runtime.txt
└── README.md
```

---

## MODELE DANYCH

### Contact
```python
class Contact(models.Model):
    STATUS_CHOICES = [
        ('lead', 'Lead'),
        ('prospect', 'Prospect'),
        ('customer', 'Customer'),
        ('churned', 'Churned'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    position = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='lead')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Company
```python
class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Interaction
```python
class Interaction(models.Model):
    TYPE_CHOICES = [
        ('note', 'Note'),
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
    ]
    
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='interactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='note')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

### Task
```python
class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]
    
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

---

## PLAN IMPLEMENTACJI Z COMMITAMI

### FAZA 1: Dokumentacja i Setup (Dzień 1)

```bash
# Commit 1
git commit -m "docs: dodaj PRD projektu Mini CRM"

# Commit 2
git commit -m "docs: dodaj specyfikację techniczną i user stories"

# Commit 3
git commit -m "chore: inicjalizacja projektu Django z podstawową konfiguracją"

# Commit 4
git commit -m "chore: dodaj .gitignore, requirements.txt i README"
```

### FAZA 2: Autentykacja (Dzień 2)

```bash
# Commit 5
git commit -m "feat(accounts): dodaj aplikację accounts z modelem użytkownika"

# Commit 6
git commit -m "feat(accounts): dodaj widoki logowania i rejestracji"

# Commit 7
git commit -m "feat(accounts): dodaj szablony auth i formularz profilu"

# Commit 8
git commit -m "feat: dodaj bazowy szablon i nawigację"

# Commit 9
git commit -m "test(accounts): dodaj testy jednostkowe dla auth"
```

### FAZA 3: CRUD Kontaktów (Dzień 3-4)

```bash
# Commit 10
git commit -m "feat(contacts): dodaj model Contact i Company"

# Commit 11
git commit -m "feat(contacts): dodaj widoki CRUD dla kontaktów"

# Commit 12
git commit -m "feat(contacts): dodaj szablony listy i formularzy kontaktów"

# Commit 13
git commit -m "feat(contacts): dodaj wyszukiwanie i filtrowanie kontaktów"

# Commit 14
git commit -m "feat(contacts): dodaj widoki CRUD dla firm"

# Commit 15
git commit -m "test(contacts): dodaj testy dla modułu kontaktów"
```

### FAZA 4: Interakcje i Zadania (Dzień 5)

```bash
# Commit 16
git commit -m "feat(interactions): dodaj model i widoki interakcji"

# Commit 17
git commit -m "feat(interactions): dodaj timeline na stronie kontaktu"

# Commit 18
git commit -m "feat(tasks): dodaj model i widoki zadań"

# Commit 19
git commit -m "feat(tasks): dodaj listę zadań na dziś na dashboard"

# Commit 20
git commit -m "test(tasks): dodaj testy dla modułu zadań"
```

### FAZA 5: Integracja AI (Dzień 6)

```bash
# Commit 21
git commit -m "feat(ai): dodaj serwis integracji z Claude API"

# Commit 22
git commit -m "feat(ai): dodaj generowanie podsumowania kontaktu"

# Commit 23
git commit -m "feat(ai): dodaj sugestie następnych kroków"

# Commit 24
git commit -m "test(ai): dodaj testy dla modułu AI z mockami"
```

### FAZA 6: Dashboard i UI (Dzień 7)

```bash
# Commit 25
git commit -m "feat(dashboard): dodaj stronę główną z podsumowaniem"

# Commit 26
git commit -m "style: dodaj Tailwind CSS i popraw wygląd UI"

# Commit 27
git commit -m "feat: dodaj responsywność i mobile-friendly design"
```

### FAZA 7: Testy E2E i CI/CD (Dzień 8)

```bash
# Commit 28
git commit -m "test(e2e): dodaj test Playwright dla user journey"

# Commit 29
git commit -m "ci: dodaj GitHub Actions workflow"

# Commit 30
git commit -m "ci: dodaj konfigurację deployment na Railway"
```

### FAZA 8: Deployment i Finalizacja (Dzień 9-10)

```bash
# Commit 31
git commit -m "chore: konfiguracja produkcyjna (PostgreSQL, whitenoise)"

# Commit 32
git commit -m "docs: aktualizuj README z instrukcją instalacji"

# Commit 33
git commit -m "fix: poprawki po code review"

# Commit 34
git commit -m "release: wersja 1.0.0 - gotowa do zaliczenia"
```

---

## KOMENDY DO WYKONANIA NA STARCIE

```bash
# 1. Utwórz katalog projektu
mkdir mini-crm
cd mini-crm

# 2. Utwórz wirtualne środowisko
python -m venv venv
source venv/bin/activate  # Linux/Mac
# lub: venv\Scripts\activate  # Windows

# 3. Zainstaluj Django
pip install django

# 4. Utwórz projekt Django
django-admin startproject mini_crm .

# 5. Zainicjalizuj repozytorium Git
git init
git add .
git commit -m "chore: inicjalizacja projektu Django"

# 6. Połącz z GitHub
git remote add origin https://github.com/TWOJ_USERNAME/mini-crm.git
git branch -M main
git push -u origin main
```

---

## WYMAGANIA (requirements.txt)

```
Django>=5.0,<6.0
python-dotenv>=1.0.0
anthropic>=0.18.0  # lub openai>=1.0.0
Pillow>=10.0.0
django-crispy-forms>=2.1
crispy-tailwind>=1.0.0
whitenoise>=6.6.0
gunicorn>=21.0.0
dj-database-url>=2.1.0
psycopg2-binary>=2.9.9
```

### requirements-dev.txt
```
-r requirements.txt
pytest>=8.0.0
pytest-django>=4.8.0
pytest-playwright>=0.4.4
playwright>=1.41.0
factory-boy>=3.3.0
coverage>=7.4.0
```

---

## KONFIGURACJA CI/CD (.github/workflows/ci.yml)

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt
          
      - name: Run migrations
        run: python manage.py migrate
        env:
          SECRET_KEY: test-secret-key
          
      - name: Run tests
        run: pytest --cov=. --cov-report=xml
        env:
          SECRET_KEY: test-secret-key
          
      - name: Install Playwright
        run: playwright install chromium
        
      - name: Run E2E tests
        run: pytest tests/e2e/ -v
        env:
          SECRET_KEY: test-secret-key

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Railway
        uses: bervProject/railway-deploy@main
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          service: mini-crm
```

---

## PRZYKŁADOWY TEST E2E (tests/e2e/test_user_journey.py)

```python
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture
def live_server_url(live_server):
    return live_server.url

def test_user_can_register_login_and_create_contact(page: Page, live_server_url: str):
    """
    Test E2E: Użytkownik rejestruje się, loguje i tworzy kontakt.
    Spełnia wymaganie: "co najmniej jeden test weryfikujący działanie z perspektywy użytkownika"
    """
    # 1. Przejdź do strony głównej
    page.goto(live_server_url)
    
    # 2. Kliknij "Zarejestruj się"
    page.click("text=Zarejestruj się")
    
    # 3. Wypełnij formularz rejestracji
    page.fill('input[name="username"]', 'testuser')
    page.fill('input[name="email"]', 'test@example.com')
    page.fill('input[name="password1"]', 'SecurePass123!')
    page.fill('input[name="password2"]', 'SecurePass123!')
    page.click('button[type="submit"]')
    
    # 4. Sprawdź przekierowanie na dashboard
    expect(page).to_have_url(f"{live_server_url}/dashboard/")
    
    # 5. Kliknij "Dodaj kontakt"
    page.click("text=Dodaj kontakt")
    
    # 6. Wypełnij formularz kontaktu
    page.fill('input[name="first_name"]', 'Jan')
    page.fill('input[name="last_name"]', 'Kowalski')
    page.fill('input[name="email"]', 'jan.kowalski@firma.pl')
    page.fill('input[name="phone"]', '+48 123 456 789')
    page.select_option('select[name="status"]', 'lead')
    page.click('button[type="submit"]')
    
    # 7. Sprawdź czy kontakt pojawił się na liście
    expect(page.locator("text=Jan Kowalski")).to_be_visible()
    
    # 8. Kliknij w kontakt aby zobaczyć szczegóły
    page.click("text=Jan Kowalski")
    
    # 9. Sprawdź szczegóły kontaktu
    expect(page.locator("text=jan.kowalski@firma.pl")).to_be_visible()
    expect(page.locator("text=Lead")).to_be_visible()
    
    # 10. Wyloguj się
    page.click("text=Wyloguj")
    expect(page).to_have_url(f"{live_server_url}/")
```

---

## WSKAZÓWKI DLA AGENTA

### Zasady pracy:
1. **Jeden commit = jedna logiczna zmiana** - nie łącz wielu funkcjonalności w jednym commicie
2. **Najpierw dokumentacja** - zacznij od PRD.md przed pisaniem kodu
3. **Testy przy każdej funkcjonalności** - nie zostawiaj testów na koniec
4. **Sprawdzaj działanie** - po każdej funkcjonalności uruchom `python manage.py runserver` i sprawdź manualnie
5. **Commituj często** - lepiej więcej małych commitów niż jeden wielki

### Konwencja commitów (Conventional Commits):
- `feat:` - nowa funkcjonalność
- `fix:` - naprawa błędu
- `docs:` - dokumentacja
- `style:` - formatowanie, bez zmian w logice
- `refactor:` - refaktoryzacja kodu
- `test:` - dodanie/modyfikacja testów
- `chore:` - zmiany w konfiguracji, narzędziach

### Priorytety:
1. Działająca autentykacja
2. CRUD kontaktów
3. Testy
4. CI/CD
5. AI (można uprościć jeśli brakuje czasu)
6. Deployment

---

## PYTANIA DO UŻYTKOWNIKA NA STARCIE

Zanim zaczniesz, zapytaj użytkownika:
1. Czy ma już założone repozytorium na GitHub?
2. Czy ma zainstalowany Python 3.10+?
3. Czy ma klucz API do Claude/OpenAI?
4. Jaki system operacyjny używa (Windows/Mac/Linux)?
5. Czy preferuje Tailwind CSS czy Bootstrap?

---

## ROZPOCZNIJ PRACĘ

Teraz jestem gotowy do pracy. Zacznij od:
1. Sprawdzenia środowiska użytkownika
2. Utworzenia struktury katalogów
3. Napisania PRD.md
4. Inicjalizacji projektu Django

Pytaj o każdy krok i czekaj na potwierdzenie przed przejściem dalej. Po każdej znaczącej zmianie przypominaj o wykonaniu commita.
