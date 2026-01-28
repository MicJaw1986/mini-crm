"""
Testy dla modeli Contact i Company

CZYTAJ UWAŻNIE KOMENTARZE - Wszystko jest wyjaśnione krok po kroku!
"""

from django.test import TestCase
from django.contrib.auth.models import User
from contacts.models import Contact, Company


class TestContactModel(TestCase):
    """
    Klasa testowa dla modelu Contact.

    UWAGA: Dziedziczy po TestCase z Django, co daje nam:
    - Tymczasową bazę danych (usuwana po testach)
    - Metody sprawdzające (assertEqual, assertTrue, etc.)
    - Izolację testów (każdy test zaczyna od czystej bazy)
    """

    def setUp(self):
        """
        Ta metoda uruchamia się PRZED KAŻDYM testem.

        Dlaczego to przydatne?
        - Nie musimy w każdym teście tworzyć użytkownika i kontaktu
        - Kod jest czystszy i łatwiejszy do utrzymania
        - Każdy test dostaje te same "czyste" dane
        """
        # Krok 1: Tworzymy użytkownika testowego
        # UWAGA: create_user haszuje hasło automatycznie
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

        # Krok 2: Tworzymy kontakt należący do tego użytkownika
        self.contact = Contact.objects.create(
            first_name='Jan',
            last_name='Kowalski',
            email='jan.kowalski@example.com',
            phone='+48123456789',
            status='lead',
            owner=self.user
        )

    def test_contact_creation(self):
        """
        Test 1: Sprawdzamy czy kontakt został utworzony poprawnie

        Co testujemy?
        - Czy obiekt istnieje
        - Czy jest właściwego typu
        - Czy pola mają poprawne wartości
        """
        # Sprawdź czy contact to obiekt klasy Contact
        self.assertIsInstance(self.contact, Contact)

        # Sprawdź wartości pól
        self.assertEqual(self.contact.first_name, 'Jan')
        self.assertEqual(self.contact.last_name, 'Kowalski')
        self.assertEqual(self.contact.email, 'jan.kowalski@example.com')
        self.assertEqual(self.contact.status, 'lead')
        self.assertEqual(self.contact.owner, self.user)

    def test_get_full_name_method(self):
        """
        Test 2: Sprawdzamy metodę get_full_name()

        DLACZEGO to ważne?
        - get_full_name() to logika biznesowa
        - Używamy jej w wielu miejscach (szablony, widoki)
        - Jeśli ktoś ją zmieni, test powie nam czy działa
        """
        # Wywołaj metodę
        full_name = self.contact.get_full_name()

        # Sprawdź wynik
        expected = 'Jan Kowalski'
        self.assertEqual(full_name, expected)

    def test_str_method(self):
        """
        Test 3: Sprawdzamy __str__() - reprezentację tekstową

        DLACZEGO to ważne?
        - __str__ używany jest w admin panel Django
        - Pokazuje się w select'ach w formularzach
        - Ułatwia debugging (gdy printujemy obiekt)
        """
        contact_str = str(self.contact)
        expected = 'Jan Kowalski'
        self.assertEqual(contact_str, expected)

    def test_contact_with_company(self):
        """
        Test 4: Sprawdzamy powiązanie Contact z Company

        Co testujemy?
        - Czy możemy przypisać kontakt do firmy
        - Czy relacja ForeignKey działa
        """
        # Tworzymy firmę
        company = Company.objects.create(
            name='Test Company',
            owner=self.user
        )

        # Przypisujemy kontakt do firmy
        self.contact.company = company
        self.contact.save()

        # Sprawdzamy relację
        self.assertEqual(self.contact.company, company)
        # Sprawdzamy relację odwrotną (z firmy do kontaktów)
        self.assertIn(self.contact, company.contacts.all())

    def test_get_tags_list_method(self):
        """
        Test 5: Sprawdzamy metodę get_tags_list()

        Testujemy różne przypadki (edge cases):
        1. Brak tagów (puste pole)
        2. Jeden tag
        3. Wiele tagów
        """
        # Przypadek 1: Brak tagów
        self.contact.tags = ''
        result = self.contact.get_tags_list()
        self.assertEqual(result, [])

        # Przypadek 2: Jeden tag
        self.contact.tags = 'vip'
        result = self.contact.get_tags_list()
        self.assertEqual(result, ['vip'])

        # Przypadek 3: Wiele tagów (ze spacjami)
        self.contact.tags = 'vip, partner, złoty klient'
        result = self.contact.get_tags_list()
        # Sprawdzamy czy są 3 tagi i czy są oczyszczone ze spacji
        self.assertEqual(len(result), 3)
        self.assertIn('vip', result)
        self.assertIn('partner', result)
        self.assertIn('złoty klient', result)

    def test_contact_status_choices(self):
        """
        Test 6: Sprawdzamy czy statusy działają

        DLACZEGO to ważne?
        - STATUS_CHOICES definiuje dozwolone wartości
        - Musimy wiedzieć czy zmiany w choices nie zepsują kodu
        """
        # Sprawdzamy czy możemy ustawić każdy status
        for status_code, status_name in Contact.STATUS_CHOICES:
            self.contact.status = status_code
            self.contact.save()
            self.assertEqual(self.contact.status, status_code)

    def test_unique_email_constraint(self):
        """
        Test 7: Sprawdzamy unikalność email

        UWAGA: Email powinien być unikalny w bazie!
        Testujemy czy Django to egzekwuje.
        """
        from django.db import IntegrityError

        # Próbujemy utworzyć kontakt z tym samym emailem
        with self.assertRaises(IntegrityError):
            Contact.objects.create(
                first_name='Inny',
                last_name='Człowiek',
                email='jan.kowalski@example.com',  # Ten sam email!
                owner=self.user
            )


class TestCompanyModel(TestCase):
    """
    Testy dla modelu Company

    Struktura podobna jak dla Contact
    """

    def setUp(self):
        """Przygotowanie danych testowych"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        self.company = Company.objects.create(
            name='Acme Corp',
            nip='1234567890',
            industry='IT',
            city='Warszawa',
            owner=self.user
        )

    def test_company_creation(self):
        """Test: Tworzenie firmy"""
        self.assertIsInstance(self.company, Company)
        self.assertEqual(self.company.name, 'Acme Corp')
        self.assertEqual(self.company.nip, '1234567890')

    def test_str_method(self):
        """Test: __str__ zwraca nazwę firmy"""
        self.assertEqual(str(self.company), 'Acme Corp')

    def test_get_full_address_method(self):
        """
        Test: Metoda get_full_address()

        Sprawdzamy różne przypadki:
        1. Pełny adres (wszystkie pola)
        2. Częściowy adres (brak niektórych pól)
        3. Brak adresu
        """
        # Przypadek 1: Pełny adres
        self.company.street = 'ul. Testowa 123'
        self.company.postal_code = '00-000'
        self.company.city = 'Warszawa'
        self.company.country = 'Polska'
        self.company.save()

        address = self.company.get_full_address()
        self.assertIn('Testowa', address)
        self.assertIn('Warszawa', address)
        self.assertIn('Polska', address)

        # Przypadek 2: Brak miasta
        self.company.city = ''
        address = self.company.get_full_address()
        # Sprawdzamy czy metoda nie crashuje
        self.assertIsInstance(address, str)

    def test_nip_validation(self):
        """
        Test: Walidacja NIP (10 cyfr)

        UWAGA: NIP powinien mieć dokładnie 10 cyfr
        """
        from django.core.exceptions import ValidationError

        # NIP z literami - powinien być odrzucony
        company = Company(
            name='Test',
            nip='123ABC7890',  # Zawiera litery!
            owner=self.user
        )

        # Próbujemy zwalidować
        with self.assertRaises(ValidationError):
            company.full_clean()  # full_clean() uruchamia walidatory

    def test_company_with_contacts_count(self):
        """
        Test: Sprawdzamy ile firma ma kontaktów

        Relacja odwrotna: company.contacts.all()
        """
        # Na początku 0 kontaktów
        self.assertEqual(self.company.contacts.count(), 0)

        # Dodajemy kontakt
        Contact.objects.create(
            first_name='Jan',
            last_name='Kowalski',
            email='jan@example.com',
            company=self.company,
            owner=self.user
        )

        # Teraz powinien być 1 kontakt
        self.assertEqual(self.company.contacts.count(), 1)

        # Dodajemy drugi
        Contact.objects.create(
            first_name='Anna',
            last_name='Nowak',
            email='anna@example.com',
            company=self.company,
            owner=self.user
        )

        # Teraz 2 kontakty
        self.assertEqual(self.company.contacts.count(), 2)


# PODSUMOWANIE CO NAUCZYŁEŚ SIĘ:
# 1. setUp() - przygotowanie danych przed każdym testem
# 2. assertEqual() - sprawdzanie równości
# 3. assertIn() - sprawdzanie czy element jest w kolekcji
# 4. assertRaises() - sprawdzanie czy został rzucony wyjątek
# 5. Testowanie metod modelu (get_full_name, __str__, etc.)
# 6. Testowanie relacji ForeignKey
# 7. Testowanie edge cases (puste wartości, niepoprawne dane)
