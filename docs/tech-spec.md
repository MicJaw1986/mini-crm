# Specyfikacja Techniczna
## Mini CRM - System Zarządzania Relacjami z Klientami

**Wersja:** 1.0.0
**Data:** 2026-01-17

---

## 1. Architektura Aplikacji

### 1.1 Wzorzec Architektoniczny
**MTV (Model-Template-View)** - standardowy wzorzec Django:
- **Model** - logika biznesowa i dostęp do danych
- **Template** - warstwa prezentacji (HTML + Bootstrap)
- **View** - kontroler obsługujący żądania HTTP

### 1.2 Diagram Architektury
```
┌─────────────────────────────────────────────────────────┐
│                    Browser (Client)                      │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/HTTPS
┌────────────────────▼────────────────────────────────────┐
│                    Web Server (Gunicorn)                 │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Django Application                      │
│  ┌──────────────────────────────────────────────────┐   │
│  │  URLs Router                                      │   │
│  └──────────┬───────────────────────────────────────┘   │
│             │                                            │
│  ┌──────────▼───────────┬──────────────┬──────────────┐ │
│  │  Views               │  Forms       │  Middleware  │ │
│  └──────────┬───────────┴──────────────┴──────────────┘ │
│             │                                            │
│  ┌──────────▼───────────────────────────────────────┐   │
│  │  Models (ORM)                                     │   │
│  └──────────┬───────────────────────────────────────┘   │
└─────────────┼────────────────────────────────────────────┘
              │
┌─────────────▼────────────────────────────────────────┐
│         Database (SQLite / PostgreSQL)                │
└──────────────────────────────────────────────────────┘
```

---

## 2. Stack Technologiczny

### 2.1 Backend
- **Framework:** Django 5.x
- **Język:** Python 3.12+
- **ORM:** Django ORM
- **Serwer WSGI:** Gunicorn (produkcja)
- **Serwer Dev:** Django runserver

### 2.2 Frontend
- **Template Engine:** Django Templates (Jinja2-like)
- **CSS Framework:** Bootstrap 5.3
- **Icons:** Bootstrap Icons
- **JavaScript:** Vanilla JS (minimalne użycie)

### 2.3 Baza Danych
- **Development:** SQLite3 (domyślna)
- **Production:** PostgreSQL 15+
- **Migracje:** Django Migrations

### 2.4 Testy
- **Unit Tests:** pytest + pytest-django
- **E2E Tests:** Playwright
- **Coverage:** pytest-cov
- **Fixtures:** factory-boy (opcjonalnie)

### 2.5 CI/CD
- **Pipeline:** GitHub Actions
- **Linting:** flake8 / ruff (opcjonalnie)
- **Format:** black (opcjonalnie)

### 2.6 Deployment
- **Platforma:** Railway / Render / Fly.io
- **Static Files:** WhiteNoise
- **Environment:** python-dotenv
- **Process Manager:** Gunicorn

### 2.7 AI Integration (Opcjonalne)
- **API:** Anthropic Claude API
- **Biblioteka:** anthropic-sdk
- **Backup:** OpenAI API (alternatywa)

---

## 3. Struktura Projektu

```
mini-crm/
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI/CD
│
├── docs/
│   ├── PRD.md                     # Product Requirements Document
│   ├── tech-spec.md               # Ten dokument
│   └── user-stories.md            # User stories
│
├── mini_crm/                      # Django project root
│   ├── __init__.py
│   ├── settings.py                # Główna konfiguracja
│   ├── urls.py                    # URL routing główny
│   ├── wsgi.py                    # WSGI entry point
│   └── asgi.py                    # ASGI entry point
│
├── accounts/                      # Aplikacja autentykacji
│   ├── migrations/
│   ├── templates/
│   │   └── accounts/
│   │       ├── login.html
│   │       ├── register.html
│   │       └── profile.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py                   # UserRegistrationForm, LoginForm
│   ├── models.py                  # User (Django built-in)
│   ├── urls.py
│   └── views.py                   # LoginView, RegisterView, ProfileView
│
├── contacts/                      # Aplikacja kontaktów i firm
│   ├── migrations/
│   ├── templates/
│   │   └── contacts/
│   │       ├── contact_list.html
│   │       ├── contact_detail.html
│   │       ├── contact_form.html
│   │       ├── company_list.html
│   │       ├── company_detail.html
│   │       └── company_form.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py                   # ContactForm, CompanyForm
│   ├── models.py                  # Contact, Company
│   ├── urls.py
│   └── views.py                   # CRUD views
│
├── interactions/                  # Aplikacja interakcji
│   ├── migrations/
│   ├── templates/
│   │   └── interactions/
│   │       └── interaction_form.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py                   # InteractionForm
│   ├── models.py                  # Interaction
│   ├── urls.py
│   └── views.py
│
├── tasks/                         # Aplikacja zadań
│   ├── migrations/
│   ├── templates/
│   │   └── tasks/
│   │       ├── task_list.html
│   │       └── task_form.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py                   # TaskForm
│   ├── models.py                  # Task
│   ├── urls.py
│   └── views.py
│
├── ai_assistant/                  # Aplikacja AI (opcjonalna)
│   ├── __init__.py
│   ├── apps.py
│   ├── services.py                # ClaudeService
│   └── views.py                   # AI endpoint views
│
├── templates/                     # Globalne szablony
│   ├── base.html                  # Bazowy template
│   ├── navbar.html                # Nawigacja
│   ├── dashboard.html             # Dashboard
│   └── 404.html                   # Error pages
│
├── static/
│   ├── css/
│   │   └── custom.css
│   ├── js/
│   │   └── main.js
│   └── images/
│       └── logo.png
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Pytest configuration
│   ├── test_accounts.py
│   ├── test_contacts.py
│   ├── test_companies.py
│   ├── test_interactions.py
│   ├── test_tasks.py
│   └── e2e/
│       └── test_user_journey.py   # Playwright E2E
│
├── .env.example                   # Przykładowy plik zmiennych środowiskowych
├── .gitignore
├── manage.py                      # Django management script
├── requirements.txt               # Produkcyjne zależności
├── requirements-dev.txt           # Zależności deweloperskie
├── pytest.ini                     # Konfiguracja pytest
├── Procfile                       # Dla Railway/Heroku
├── runtime.txt                    # Wersja Pythona dla hostingu
└── README.md                      # Dokumentacja projektu
```

---

## 4. Modele Danych (Szczegółowo)

### 4.1 Diagram ERD
```
┌─────────────┐
│    User     │
│ (Django)    │
└──────┬──────┘
       │
       │ 1:N
       │
       ├────────────┬────────────┬────────────┬
       │            │            │            │
┌──────▼──────┐ ┌──▼──────┐ ┌──▼─────────┐ ┌▼──────────┐
│   Company   │ │ Contact │ │Interaction │ │   Task    │
└──────┬──────┘ └────┬────┘ └────────────┘ └───────────┘
       │             │
       │ 1:N         │ 1:N
       └─────────────┘
```

### 4.2 Model: User
```python
# Wykorzystujemy built-in model Django
from django.contrib.auth.models import User

# Opcjonalnie można rozszerzyć o profil:
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    phone = models.CharField(max_length=20, blank=True)
```

### 4.3 Model: Company
```python
class Company(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='companies'
    )
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['name']
        indexes = [
            models.Index(fields=['user', 'name']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('contacts:company-detail', kwargs={'pk': self.pk})
```

### 4.4 Model: Contact
```python
class Contact(models.Model):
    STATUS_CHOICES = [
        ('lead', 'Lead'),
        ('prospect', 'Prospect'),
        ('customer', 'Customer'),
        ('churned', 'Churned'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='contacts'
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contacts'
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    position = models.CharField(max_length=100, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='lead'
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['user', 'last_name']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse('contacts:contact-detail', kwargs={'pk': self.pk})

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
```

### 4.5 Model: Interaction
```python
class Interaction(models.Model):
    TYPE_CHOICES = [
        ('note', 'Note'),
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
    ]

    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name='interactions'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='interactions'
    )
    interaction_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='note'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_interaction_type_display()} - {self.contact.full_name}"
```

### 4.6 Model: Task
```python
class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name='tasks',
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='todo'
    )
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'status', 'due_date']),
        ]

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        from django.utils import timezone
        if self.due_date and self.status != 'done':
            return self.due_date < timezone.now().date()
        return False
```

---

## 5. Widoki i URL Routing

### 5.1 URL Structure
```
/                               → Landing page / redirect to dashboard
/accounts/login/                → Login
/accounts/register/             → Register
/accounts/logout/               → Logout
/accounts/profile/              → User profile
/dashboard/                     → Main dashboard

/contacts/                      → Contact list
/contacts/create/               → Create contact
/contacts/<id>/                 → Contact detail
/contacts/<id>/edit/            → Edit contact
/contacts/<id>/delete/          → Delete contact

/companies/                     → Company list
/companies/create/              → Create company
/companies/<id>/                → Company detail
/companies/<id>/edit/           → Edit company
/companies/<id>/delete/         → Delete company

/contacts/<id>/interactions/create/  → Add interaction
/interactions/<id>/delete/           → Delete interaction

/tasks/                         → Task list
/tasks/create/                  → Create task
/tasks/<id>/edit/               → Edit task
/tasks/<id>/delete/             → Delete task
/tasks/<id>/toggle/             → Toggle task status

/ai/summarize/<contact_id>/     → Generate AI summary (optional)
```

### 5.2 Views Architecture
- **Function-Based Views (FBV)** - dla prostych operacji
- **Class-Based Views (CBV)** - dla CRUD (ListView, DetailView, CreateView, UpdateView, DeleteView)

Przykład:
```python
# contacts/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'contacts/contact_list.html'
    context_object_name = 'contacts'
    paginate_by = 20

    def get_queryset(self):
        # Tylko kontakty zalogowanego użytkownika
        queryset = Contact.objects.filter(user=self.request.user)

        # Filtrowanie po statusie
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Wyszukiwanie
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )

        return queryset
```

---

## 6. Bezpieczeństwo

### 6.1 Autentykacja i Autoryzacja
- **LoginRequiredMixin** - wymuszenie logowania dla widoków CBV
- **@login_required** - dekorator dla widoków FBV
- **User isolation** - każdy model filtruje po `user=request.user`

### 6.2 Ochrona CSRF
- Django CSRF middleware aktywne domyślnie
- Wszystkie formularze zawierają `{% csrf_token %}`

### 6.3 Walidacja Danych
- Django Forms z automatyczną walidacją
- Custom validators dla email, phone
- Sanityzacja HTML w notatках (bleach library opcjonalnie)

### 6.4 Bezpieczne Hasła
- Django PBKDF2 password hasher (domyślny)
- Minimum 8 znaków, walidacja w formularzu rejestracji

### 6.5 Environment Variables
```python
# settings.py
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')
DATABASE_URL = os.getenv('DATABASE_URL')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
```

---

## 7. Testy

### 7.1 Testy Jednostkowe (pytest)
```python
# tests/test_contacts.py
import pytest
from django.contrib.auth.models import User
from contacts.models import Contact, Company

@pytest.mark.django_db
def test_contact_creation():
    user = User.objects.create_user('testuser', 'test@test.com', 'password')
    contact = Contact.objects.create(
        user=user,
        first_name='John',
        last_name='Doe',
        email='john@example.com',
        status='lead'
    )
    assert contact.full_name == 'John Doe'
    assert str(contact) == 'John Doe'

@pytest.mark.django_db
def test_user_isolation():
    user1 = User.objects.create_user('user1', 'user1@test.com', 'pass')
    user2 = User.objects.create_user('user2', 'user2@test.com', 'pass')

    Contact.objects.create(user=user1, first_name='Alice', last_name='Smith')
    Contact.objects.create(user=user2, first_name='Bob', last_name='Jones')

    assert Contact.objects.filter(user=user1).count() == 1
    assert Contact.objects.filter(user=user2).count() == 1
```

### 7.2 Test E2E (Playwright)
```python
# tests/e2e/test_user_journey.py
def test_complete_user_journey(page, live_server):
    # 1. Register
    page.goto(f"{live_server.url}/accounts/register/")
    page.fill('input[name="username"]', 'testuser')
    page.fill('input[name="password1"]', 'SecurePass123!')
    page.fill('input[name="password2"]', 'SecurePass123!')
    page.click('button[type="submit"]')

    # 2. Create contact
    page.click("text=Add Contact")
    page.fill('input[name="first_name"]', 'John')
    page.fill('input[name="last_name"]', 'Doe')
    page.click('button[type="submit"]')

    # 3. Verify
    expect(page.locator("text=John Doe")).to_be_visible()
```

### 7.3 Pokrycie Testami
- Unit tests: modele, formularze, podstawowe widoki
- Integration tests: pełne CRUD flow
- E2E test: co najmniej 1 scenariusz użytkownika
- Target coverage: 70%+

---

## 8. CI/CD Pipeline

### 8.1 GitHub Actions Workflow
```yaml
name: CI/CD

on: [push, pull_request]

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
        run: pip install -r requirements-dev.txt
      - name: Run migrations
        run: python manage.py migrate
      - name: Run tests
        run: pytest --cov
      - name: Run E2E
        run: |
          playwright install chromium
          pytest tests/e2e/
```

---

## 9. Deployment

### 9.1 Konfiguracja Produkcyjna
```python
# settings.py
import dj_database_url

if not DEBUG:
    # PostgreSQL
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600)
    }

    # Static files
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    # Security
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

### 9.2 Procfile (Railway/Heroku)
```
web: gunicorn mini_crm.wsgi:application
release: python manage.py migrate
```

### 9.3 runtime.txt
```
python-3.12.1
```

---

## 10. Skalowanie i Optymalizacja (Future)

### 10.1 Caching
- Redis dla sesji
- Django cache framework
- Template fragment caching

### 10.2 Query Optimization
- `select_related()` dla ForeignKey
- `prefetch_related()` dla Many-to-Many
- Database indexing (już dodane w modelach)

### 10.3 Monitoring
- Sentry dla error tracking
- Django Debug Toolbar (dev only)
- Application Performance Monitoring (opcjonalnie)

---

## Podsumowanie

Ta specyfikacja techniczna definiuje:
- ✅ Architekturę MTV opartą na Django
- ✅ Szczegółowe modele danych z relacjami
- ✅ Struktura URL i widoków
- ✅ Strategia bezpieczeństwa
- ✅ Plan testów (unit + E2E)
- ✅ Pipeline CI/CD
- ✅ Procedura deploymentu

Dokument ten służy jako referencyjna implementacja dla projektu Mini CRM.
