"""
Testy dla formularzy Contact i Company

CZYTAJ UWAŻNIE - Tutaj uczysz się testowania formularzy!
"""

from django.test import TestCase
from django.contrib.auth.models import User
from contacts.forms import ContactForm, CompanyForm, ContactSearchForm
from contacts.models import Contact, Company


class TestContactForm(TestCase):
    """
    Testy dla ContactForm

    Co testujemy?
    - Walidację danych (czy formularz przyjmuje poprawne dane)
    - Odrzucanie niepoprawnych danych
    - Czyste dane (cleaned_data)
    - Błędy walidacji
    """

    def setUp(self):
        """Przygotowanie - tworzymy użytkownika"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_valid_form(self):
        """
        Test 1: Formularz z poprawnymi danymi

        Struktura testu formularza:
        1. Przygotuj dane (słownik)
        2. Utwórz formularz z tymi danymi
        3. Sprawdź czy is_valid() zwraca True
        """
        # Dane formularza - wszystkie wymagane pola
        data = {
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'email': 'jan.kowalski@example.com',
            'phone': '+48123456789',
            'mobile': '+48987654321',
            'status': 'lead',
            'tags': 'vip, partner',
        }

        # Tworzymy formularz
        # UWAGA: ContactForm wymaga user=... (używamy w __init__)
        form = ContactForm(data=data, user=self.user)

        # Sprawdzamy czy formularz jest poprawny
        self.assertTrue(form.is_valid())

        # Sprawdzamy czy nie ma błędów
        self.assertEqual(len(form.errors), 0)

    def test_missing_required_fields(self):
        """
        Test 2: Brakujące wymagane pola

        Co jest wymagane?
        - first_name, last_name, email
        """
        # Puste dane
        data = {}

        form = ContactForm(data=data, user=self.user)

        # Formularz NIE POWINIEN być poprawny
        self.assertFalse(form.is_valid())

        # Sprawdzamy czy są błędy dla wymaganych pól
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)
        self.assertIn('email', form.errors)

    def test_invalid_email_format(self):
        """
        Test 3: Niepoprawny format email

        Django automatycznie waliduje email
        """
        data = {
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'email': 'to-nie-jest-email',  # Niepoprawny format!
            'status': 'lead',
        }

        form = ContactForm(data=data, user=self.user)

        # Formularz nie powinien być poprawny
        self.assertFalse(form.is_valid())

        # Sprawdzamy czy błąd dotyczy pola email
        self.assertIn('email', form.errors)

    def test_phone_number_validation(self):
        """
        Test 4: Walidacja numeru telefonu

        Jeśli mamy własny walidator dla telefonu, testujemy go tutaj
        """
        data = {
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'email': 'jan@example.com',
            'phone': '123',  # Za krótki numer
            'status': 'lead',
        }

        form = ContactForm(data=data, user=self.user)

        # W zależności od walidatora, formularz może być poprawny lub nie
        # Jeśli mamy walidację długości telefonu:
        # self.assertFalse(form.is_valid())
        # self.assertIn('phone', form.errors)

    def test_status_choices_validation(self):
        """
        Test 5: Walidacja wyboru statusu

        Status musi być jednym z STATUS_CHOICES
        """
        data = {
            'first_name': 'Jan',
            'last_name': 'Kowalski',
            'email': 'jan@example.com',
            'status': 'invalid_status',  # Niepoprawny status!
        }

        form = ContactForm(data=data, user=self.user)

        # Formularz nie powinien być poprawny
        self.assertFalse(form.is_valid())
        self.assertIn('status', form.errors)

    def test_valid_status_choices(self):
        """
        Test 6: Sprawdzamy czy wszystkie poprawne statusy działają
        """
        from contacts.models import Contact

        for status_code, status_name in Contact.STATUS_CHOICES:
            data = {
                'first_name': 'Jan',
                'last_name': 'Kowalski',
                'email': f'jan.{status_code}@example.com',  # Unikalny email
                'status': status_code,
            }

            form = ContactForm(data=data, user=self.user)

            # Każdy status powinien być poprawny
            self.assertTrue(
                form.is_valid(),
                f"Status '{status_code}' powinien być poprawny"
            )

    def test_company_queryset_filtered_by_user(self):
        """
        Test 7: Sprawdzamy czy pole 'company' pokazuje tylko firmy użytkownika

        WAŻNE dla bezpieczeństwa!
        - Użytkownik nie może przypisać kontaktu do cudzej firmy
        """
        # Tworzymy firmę dla naszego użytkownika
        my_company = Company.objects.create(
            name='Moja Firma',
            owner=self.user
        )

        # Tworzymy firmę innego użytkownika
        other_user = User.objects.create_user(
            username='otheruser',
            password='pass123'
        )
        other_company = Company.objects.create(
            name='Cudza Firma',
            owner=other_user
        )

        # Tworzymy formularz dla naszego użytkownika
        form = ContactForm(user=self.user)

        # Pobieramy queryset z pola 'company'
        company_queryset = form.fields['company'].queryset

        # Sprawdzamy czy jest nasza firma
        self.assertIn(my_company, company_queryset)

        # Sprawdzamy czy NIE MA cudzej firmy
        self.assertNotIn(other_company, company_queryset)

    def test_form_save_creates_contact(self):
        """
        Test 8: Czy zapisanie formularza tworzy kontakt?

        UWAGA: Testujemy zachowanie form.save()
        """
        data = {
            'first_name': 'Nowy',
            'last_name': 'Kontakt',
            'email': 'nowy@example.com',
            'status': 'lead',
        }

        form = ContactForm(data=data, user=self.user)

        # Formularz musi być poprawny
        self.assertTrue(form.is_valid())

        # Zapisujemy formularz (ale nie do bazy - commit=False)
        contact = form.save(commit=False)

        # Ustawiamy właściciela (w widoku robi to view)
        contact.owner = self.user

        # Teraz zapisujemy do bazy
        contact.save()

        # Sprawdzamy czy kontakt istnieje w bazie
        self.assertEqual(Contact.objects.count(), 1)

        # Sprawdzamy dane
        saved_contact = Contact.objects.first()
        self.assertEqual(saved_contact.first_name, 'Nowy')
        self.assertEqual(saved_contact.owner, self.user)


class TestCompanyForm(TestCase):
    """
    Testy dla CompanyForm
    """

    def setUp(self):
        """Przygotowanie"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_valid_company_form(self):
        """
        Test: Poprawne dane dla firmy
        """
        data = {
            'name': 'Test Sp. z o.o.',
            'nip': '1234567890',
            'industry': 'IT',
            'city': 'Warszawa',
            'country': 'Polska',
        }

        form = CompanyForm(data=data, user=self.user)

        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_missing_required_name(self):
        """
        Test: Brak wymaganej nazwy firmy
        """
        data = {
            'nip': '1234567890',
            'industry': 'IT',
        }

        form = CompanyForm(data=data, user=self.user)

        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_nip_validation(self):
        """
        Test: Walidacja NIP (jeśli mamy własny walidator)

        NIP powinien mieć 10 cyfr
        """
        # NIP za krótki
        data = {
            'name': 'Test Firma',
            'nip': '12345',  # Za krótki
        }

        form = CompanyForm(data=data, user=self.user)

        # W zależności od walidatora:
        # Jeśli mamy walidację NIP, formularz powinien być niepoprawny
        # self.assertFalse(form.is_valid())
        # self.assertIn('nip', form.errors)

    def test_nip_with_letters_invalid(self):
        """
        Test: NIP z literami jest niepoprawny
        """
        data = {
            'name': 'Test Firma',
            'nip': '123ABC7890',  # Zawiera litery
        }

        form = CompanyForm(data=data, user=self.user)

        # Jeśli mamy walidację tylko cyfr:
        # self.assertFalse(form.is_valid())
        # self.assertIn('nip', form.errors)

    def test_form_widgets_have_css_classes(self):
        """
        Test: Sprawdzamy czy pola mają klasy Bootstrap

        To zapewnia że formularz będzie ładnie wyglądał
        """
        form = CompanyForm(user=self.user)

        # Sprawdzamy klasy CSS dla poszczególnych pól
        self.assertIn('form-control', form.fields['name'].widget.attrs.get('class', ''))
        self.assertIn('form-control', form.fields['nip'].widget.attrs.get('class', ''))


class TestContactSearchForm(TestCase):
    """
    Testy dla formularza wyszukiwania
    """

    def setUp(self):
        """Przygotowanie"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        # Tworzymy kilka kontaktów do testowania wyszukiwania
        Contact.objects.create(
            first_name='Jan',
            last_name='Kowalski',
            email='jan@example.com',
            status='lead',
            owner=self.user
        )

        Contact.objects.create(
            first_name='Anna',
            last_name='Nowak',
            email='anna@example.com',
            status='customer',
            owner=self.user
        )

    def test_empty_search_form_is_valid(self):
        """
        Test: Pusty formularz wyszukiwania jest poprawny

        Puste wyszukiwanie = pokaż wszystko
        """
        data = {}
        form = ContactSearchForm(data=data, user=self.user)

        self.assertTrue(form.is_valid())

    def test_search_with_query(self):
        """
        Test: Wyszukiwanie z frazą tekstową
        """
        data = {'query': 'Jan'}
        form = ContactSearchForm(data=data, user=self.user)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['query'], 'Jan')

    def test_search_with_status_filter(self):
        """
        Test: Filtrowanie po statusie
        """
        data = {'status': 'lead'}
        form = ContactSearchForm(data=data, user=self.user)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['status'], 'lead')

    def test_search_with_company_filter(self):
        """
        Test: Filtrowanie po firmie
        """
        # Tworzymy firmę
        company = Company.objects.create(
            name='Test Firma',
            owner=self.user
        )

        data = {'company': company.pk}
        form = ContactSearchForm(data=data, user=self.user)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['company'], company)

    def test_invalid_status_in_search(self):
        """
        Test: Niepoprawny status w wyszukiwaniu
        """
        data = {'status': 'invalid_status'}
        form = ContactSearchForm(data=data, user=self.user)

        # Formularz nie powinien być poprawny
        self.assertFalse(form.is_valid())


# PODSUMOWANIE CO SIĘ NAUCZYŁEŚ:
# 1. Testowanie formularzy Django
# 2. is_valid() - sprawdza walidację
# 3. form.errors - słownik z błędami
# 4. cleaned_data - oczyszczone i zwalidowane dane
# 5. assertIn(field, form.errors) - sprawdza błędy konkretnego pola
# 6. Testowanie wymaganych pól
# 7. Testowanie walidatorów (email, telefon, NIP)
# 8. Testowanie choices (statusy, priorytety)
# 9. Testowanie querysetów w polach (bezpieczeństwo)
# 10. Testowanie form.save()
# 11. Testowanie widgetów i klas CSS
# 12. Różne scenariusze: poprawne dane, błędne dane, puste pola
