# 📖 Przewodnik po testowaniu - Od podstaw

## 🎯 Czym są testy i dlaczego są ważne?

### Co to są testy automatyczne?

**Testy automatyczne** to kod, który sprawdza czy Twoja aplikacja działa poprawnie. Zamiast ręcznie klikać po aplikacji i sprawdzać czy wszystko działa, piszesz kod, który to robi za Ciebie.

### Dlaczego warto pisać testy?

1. **Pewność** - Wiesz, że Twój kod działa
2. **Bezpieczeństwo** - Gdy coś zmieniasz, testy powiedzą Ci czy czegoś nie zepsułeś
3. **Dokumentacja** - Testy pokazują jak kod powinien działać
4. **Oszczędność czasu** - Szybsze niż ręczne testowanie
5. **Profesjonalizm** - Każdy dobry projekt ma testy

### Rodzaje testów

#### 1. **Testy jednostkowe (Unit Tests)**
- Testują małe kawałki kodu (funkcje, metody)
- Najszybsze i najłatwiejsze do napisania
- Przykład: Czy funkcja `get_full_name()` zwraca imię i nazwisko?

#### 2. **Testy integracyjne (Integration Tests)**
- Testują jak różne części współpracują
- Przykład: Czy formularz kontaktu zapisuje dane do bazy?

#### 3. **Testy E2E (End-to-End)**
- Testują całą aplikację jak prawdziwy użytkownik
- Symulują klikanie, wypełnianie formularzy
- Najwolniejsze, ale najbardziej realistyczne

## 📝 Struktura testów w Django

### Gdzie umieszczać testy?

Każda aplikacja Django ma plik `tests.py`. Dla większych projektów tworzymy folder `tests/`:

```
contacts/
├── tests/
│   ├── __init__.py
│   ├── test_models.py      # Testy modeli
│   ├── test_views.py       # Testy widoków
│   └── test_forms.py       # Testy formularzy
```

### Konwencje nazewnicze

- Pliki testów: `test_*.py` lub `*_test.py`
- Klasy testowe: `Test*` (np. `TestContactModel`)
- Metody testowe: `test_*` (np. `test_contact_creation`)

## 🧪 Anatomia testu

### Podstawowa struktura

```python
from django.test import TestCase

class TestMojKod(TestCase):
    def test_nazwa_testu(self):
        # 1. ARRANGE - przygotuj dane
        dane = "przykład"

        # 2. ACT - wykonaj akcję
        wynik = funkcja(dane)

        # 3. ASSERT - sprawdź rezultat
        self.assertEqual(wynik, "oczekiwany_rezultat")
```

### Metody sprawdzające (Assertions)

- `assertEqual(a, b)` - sprawdza czy a == b
- `assertNotEqual(a, b)` - sprawdza czy a != b
- `assertTrue(x)` - sprawdza czy x jest True
- `assertFalse(x)` - sprawdza czy x jest False
- `assertIn(a, b)` - sprawdza czy a znajduje się w b
- `assertIsNone(x)` - sprawdza czy x jest None
- `assertRaises(Error)` - sprawdza czy został rzucony błąd

## 🎓 Przykłady krok po kroku

### Przykład 1: Test modelu Contact

```python
from django.test import TestCase
from django.contrib.auth.models import User
from contacts.models import Contact

class TestContactModel(TestCase):
    """Testy dla modelu Contact"""

    def setUp(self):
        """
        Metoda setUp uruchamia się PRZED KAŻDYM testem.
        Służy do przygotowania danych testowych.
        """
        # Tworzymy użytkownika testowego
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        # Tworzymy kontakt testowy
        self.contact = Contact.objects.create(
            first_name='Jan',
            last_name='Kowalski',
            email='jan@example.com',
            owner=self.user
        )

    def test_contact_creation(self):
        """Test: Czy kontakt został utworzony poprawnie?"""
        # Sprawdzamy czy kontakt istnieje
        self.assertTrue(isinstance(self.contact, Contact))

        # Sprawdzamy pola
        self.assertEqual(self.contact.first_name, 'Jan')
        self.assertEqual(self.contact.last_name, 'Kowalski')

    def test_get_full_name(self):
        """Test: Czy metoda get_full_name działa?"""
        # Wykonujemy metodę
        full_name = self.contact.get_full_name()

        # Sprawdzamy wynik
        self.assertEqual(full_name, 'Jan Kowalski')

    def test_contact_str(self):
        """Test: Czy __str__ zwraca poprawny tekst?"""
        expected = 'Jan Kowalski'
        self.assertEqual(str(self.contact), expected)
```

### Przykład 2: Test widoku (View)

```python
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class TestContactListView(TestCase):
    """Testy dla widoku listy kontaktów"""

    def setUp(self):
        """Przygotowanie danych"""
        # Client służy do symulowania requestów HTTP
        self.client = Client()

        # Tworzymy użytkownika
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_redirect_if_not_logged_in(self):
        """Test: Czy niezalogowany użytkownik jest przekierowany?"""
        # Próbujemy wejść na listę kontaktów bez logowania
        response = self.client.get(reverse('contacts:contact_list'))

        # Sprawdzamy czy dostaliśmy przekierowanie (302)
        self.assertEqual(response.status_code, 302)

        # Sprawdzamy czy przekierowuje na login
        self.assertIn('/accounts/login/', response.url)

    def test_logged_in_can_access(self):
        """Test: Czy zalogowany użytkownik ma dostęp?"""
        # Logujemy użytkownika
        self.client.login(username='testuser', password='testpass123')

        # Próbujemy wejść na listę
        response = self.client.get(reverse('contacts:contact_list'))

        # Sprawdzamy czy dostaliśmy status 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Sprawdzamy czy użyto poprawnego szablonu
        self.assertTemplateUsed(response, 'contacts/contact_list.html')
```

### Przykład 3: Test formularza

```python
from django.test import TestCase
from contacts.forms import ContactForm

class TestContactForm(TestCase):
    """Testy dla formularza kontaktu"""

    def test_valid_form(self):
        """Test: Czy poprawne dane przechodzą walidację?"""
        # Przygotowujemy poprawne dane
        data = {
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'email': 'jan@example.com',
            'status': 'lead'
        }

        # Tworzymy formularz z tymi danymi
        form = ContactForm(data=data)

        # Sprawdzamy czy formularz jest poprawny
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        """Test: Czy niepoprawny email jest odrzucany?"""
        data = {
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'email': 'niepoprawny-email',  # Zły email
            'status': 'lead'
        }

        form = ContactForm(data=data)

        # Formularz NIE powinien być poprawny
        self.assertFalse(form.is_valid())

        # Sprawdzamy czy błąd dotyczy pola email
        self.assertIn('email', form.errors)
```

## 🚀 Uruchamianie testów

### Wszystkie testy
```bash
python manage.py test
```

### Testy konkretnej aplikacji
```bash
python manage.py test contacts
```

### Konkretny plik testów
```bash
python manage.py test contacts.tests.test_models
```

### Konkretna klasa testowa
```bash
python manage.py test contacts.tests.test_models.TestContactModel
```

### Z szczegółowym outputem
```bash
python manage.py test --verbosity=2
```

## 📊 Coverage - pokrycie kodu testami

Coverage pokazuje ile % Twojego kodu jest przetestowane.

### Instalacja
```bash
pip install coverage
```

### Uruchomienie
```bash
# Uruchom testy z pomiarem pokrycia
coverage run --source='.' manage.py test

# Zobacz raport w terminalu
coverage report

# Wygeneruj raport HTML
coverage html
# Otwórz htmlcov/index.html w przeglądarce
```

## 🎭 Playwright - Testy E2E

Playwright symuluje prawdziwego użytkownika - otwiera przeglądarkę, klika, wypełnia formularze.

### Przykład testu E2E

```python
from playwright.sync_api import sync_playwright

def test_user_login():
    """Test: Czy użytkownik może się zalogować?"""
    with sync_playwright() as p:
        # Uruchom przeglądarkę
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Wejdź na stronę logowania
        page.goto('http://localhost:8000/accounts/login/')

        # Wypełnij formularz
        page.fill('input[name="username"]', 'testuser')
        page.fill('input[name="password"]', 'testpass123')

        # Kliknij przycisk
        page.click('button[type="submit"]')

        # Poczekaj na przekierowanie
        page.wait_for_url('**/dashboard/')

        # Sprawdź czy jesteśmy na dashboardzie
        assert 'Dashboard' in page.title()

        browser.close()
```

## ✅ Dobre praktyki

1. **Test jeden przypadek** - każdy test powinien sprawdzać jedną rzecz
2. **Nazwy opisowe** - `test_user_cannot_delete_other_user_contact` zamiast `test1`
3. **Niezależność** - testy nie powinny zależeć od siebie
4. **Szybkość** - testy jednostkowe powinny być szybkie
5. **setUp i tearDown** - używaj do przygotowania i czyszczenia
6. **Fixtures** - używaj do powtarzających się danych

## 🎯 Co testować?

### Zawsze testuj:
- ✅ Logikę biznesową (metody modeli)
- ✅ Walidację formularzy
- ✅ Uprawnienia dostępu
- ✅ Krytyczne ścieżki użytkownika

### Nie musisz testować:
- ❌ Kodu Django (już przetestowany)
- ❌ Bibliotek zewnętrznych
- ❌ Prostych getterów/setterów

## 📚 Następne kroki

1. Napisz testy dla modeli (Contact, Company, Task, Interaction)
2. Przetestuj widoki (czy wymagają logowania, czy zwracają poprawne dane)
3. Przetestuj formularze (walidacja, zapisywanie)
4. Dodaj testy E2E dla kluczowych funkcji
5. Zmierz pokrycie kodu (cel: >80%)

---

**Pamiętaj**: Pisanie testów to umiejętność, którą rozwijasz z czasem. Zacznij od prostych testów i stopniowo dodawaj bardziej skomplikowane!
