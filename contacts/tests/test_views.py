"""
Testy dla widoków Contact i Company

CZYTAJ UWAŻNIE - Tutaj uczysz się testowania widoków Django!
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from contacts.models import Contact, Company


class TestContactListView(TestCase):
    """
    Testy dla widoku listy kontaktów

    Co nowego się uczysz?
    - Client: symuluje przeglądarkę (wysyła requesty HTTP)
    - reverse(): zamienia nazwę URL na ścieżkę
    - Testowanie autentykacji (czy niezalogowani są blokowani)
    - Testowanie szablonów (czy używany jest poprawny plik HTML)
    """

    def setUp(self):
        """
        Przygotowanie - tworzymy:
        1. Client (symuluje przeglądarkę)
        2. Użytkownika testowego
        3. Kilka kontaktów
        """
        # Client to narzędzie do wysyłania requestów HTTP
        self.client = Client()

        # Tworzymy użytkownika
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Tworzymy drugiego użytkownika (do testowania izolacji danych)
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )

        # Kontakty pierwszego użytkownika
        self.contact1 = Contact.objects.create(
            first_name='Jan',
            last_name='Kowalski',
            email='jan@example.com',
            status='lead',
            owner=self.user
        )

        self.contact2 = Contact.objects.create(
            first_name='Anna',
            last_name='Nowak',
            email='anna@example.com',
            status='customer',
            owner=self.user
        )

        # Kontakt drugiego użytkownika (nie powinien być widoczny dla self.user)
        self.other_contact = Contact.objects.create(
            first_name='Ktoś',
            last_name='Inny',
            email='inny@example.com',
            owner=self.other_user
        )

    def test_redirect_if_not_logged_in(self):
        """
        Test 1: Czy niezalogowany użytkownik jest przekierowany?

        DLACZEGO to ważne?
        - Zabezpieczenie danych - tylko zalogowani mają dostęp
        - Sprawdzamy czy @login_required działa
        """
        # Wysyłamy GET request BEZ logowania
        response = self.client.get(reverse('contacts:contact_list'))

        # Sprawdzamy kod statusu
        # 302 = redirect (przekierowanie)
        # 200 = OK (strona załadowana)
        # 404 = Not Found
        # 403 = Forbidden
        # 500 = Server Error
        self.assertEqual(response.status_code, 302)

        # Sprawdzamy czy przekierowuje na login
        # response.url to adres przekierowania
        self.assertIn('/accounts/login/', response.url)

    def test_logged_in_user_can_access(self):
        """
        Test 2: Czy zalogowany użytkownik ma dostęp?

        Co testujemy?
        - Czy po zalogowaniu dostajemy status 200 (OK)
        - Czy używany jest poprawny szablon
        """
        # Logujemy użytkownika
        # UWAGA: client.login() używa username i password
        self.client.login(username='testuser', password='testpass123')

        # Teraz próbujemy wejść na listę
        response = self.client.get(reverse('contacts:contact_list'))

        # Powinniśmy dostać status 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Sprawdzamy czy użyto poprawnego szablonu
        self.assertTemplateUsed(response, 'contacts/contact_list.html')

    def test_only_owner_contacts_displayed(self):
        """
        Test 3: Izolacja danych - użytkownik widzi tylko swoje kontakty

        KLUCZOWE dla bezpieczeństwa!
        - Użytkownik A nie może widzieć kontaktów użytkownika B
        """
        # Logujemy pierwszego użytkownika
        self.client.login(username='testuser', password='testpass123')

        # Pobieramy listę kontaktów
        response = self.client.get(reverse('contacts:contact_list'))

        # response.context to dane przekazane do szablonu
        # 'contacts' to nazwa zmiennej w widoku
        contacts = response.context['contacts']

        # Sprawdzamy ile kontaktów widzimy
        self.assertEqual(len(contacts), 2)  # Powinny być 2 (Jan i Anna)

        # Sprawdzamy czy nasze kontakty są na liście
        self.assertIn(self.contact1, contacts)
        self.assertIn(self.contact2, contacts)

        # WAŻNE: Sprawdzamy czy NIE MA kontaktu innego użytkownika
        self.assertNotIn(self.other_contact, contacts)

    def test_search_functionality(self):
        """
        Test 4: Wyszukiwarka kontaktów

        Testujemy czy search query działa poprawnie
        """
        self.client.login(username='testuser', password='testpass123')

        # Wysyłamy request z parametrem ?query=Jan
        # GET parameters przekazujemy przez data={}
        response = self.client.get(
            reverse('contacts:contact_list'),
            data={'query': 'Jan'}
        )

        contacts = response.context['contacts']

        # Powinien być tylko Jan Kowalski
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0].first_name, 'Jan')

    def test_filter_by_status(self):
        """
        Test 5: Filtrowanie po statusie

        Sprawdzamy czy możemy filtrować kontakty po statusie
        """
        self.client.login(username='testuser', password='testpass123')

        # Filtrujemy po statusie 'lead'
        response = self.client.get(
            reverse('contacts:contact_list'),
            data={'status': 'lead'}
        )

        contacts = response.context['contacts']

        # Powinien być tylko Jan (status='lead')
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0].status, 'lead')


class TestContactDetailView(TestCase):
    """
    Testy dla widoku szczegółów kontaktu
    """

    def setUp(self):
        """Przygotowanie danych"""
        self.client = Client()

        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )

        self.contact = Contact.objects.create(
            first_name='Jan',
            last_name='Kowalski',
            email='jan@example.com',
            owner=self.user
        )

        self.other_contact = Contact.objects.create(
            first_name='Inny',
            last_name='Użytkownik',
            email='inny@example.com',
            owner=self.other_user
        )

    def test_can_view_own_contact(self):
        """
        Test: Czy użytkownik może zobaczyć swój kontakt?
        """
        self.client.login(username='testuser', password='testpass123')

        # reverse('name', args=[id]) tworzy URL z parametrem
        # np. /contacts/1/
        response = self.client.get(
            reverse('contacts:contact_detail', args=[self.contact.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contacts/contact_detail.html')

        # Sprawdzamy czy kontakt jest w kontekście
        self.assertEqual(response.context['contact'], self.contact)

    def test_cannot_view_other_user_contact(self):
        """
        Test: Czy użytkownik NIE MOŻE zobaczyć cudzego kontaktu?

        KLUCZOWE dla bezpieczeństwa!
        """
        self.client.login(username='testuser', password='testpass123')

        # Próbujemy wejść na kontakt innego użytkownika
        response = self.client.get(
            reverse('contacts:contact_detail', args=[self.other_contact.pk])
        )

        # Powinniśmy dostać 404 (Not Found) lub 403 (Forbidden)
        # W naszym przypadku widok zwraca 404
        self.assertEqual(response.status_code, 404)

    def test_contact_detail_shows_company(self):
        """
        Test: Czy szczegóły kontaktu pokazują firmę?
        """
        # Tworzymy firmę
        company = Company.objects.create(
            name='Test Sp. z o.o.',
            owner=self.user
        )

        # Przypisujemy firmę do kontaktu
        self.contact.company = company
        self.contact.save()

        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('contacts:contact_detail', args=[self.contact.pk])
        )

        # Sprawdzamy czy firma jest w kontekście
        contact = response.context['contact']
        self.assertEqual(contact.company, company)


class TestContactCreateView(TestCase):
    """
    Testy dla tworzenia nowego kontaktu

    Co nowego?
    - Testowanie formularzy POST
    - Sprawdzanie czy dane zostały zapisane
    - Testowanie walidacji
    """

    def setUp(self):
        """Przygotowanie"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_can_create_contact_with_valid_data(self):
        """
        Test: Tworzenie kontaktu z poprawnymi danymi

        Krok po kroku:
        1. Logujemy się
        2. Wysyłamy POST z danymi
        3. Sprawdzamy czy kontakt został utworzony
        4. Sprawdzamy przekierowanie
        """
        self.client.login(username='testuser', password='testpass123')

        # Dane formularza
        data = {
            'first_name': 'Nowy',
            'last_name': 'Kontakt',
            'email': 'nowy@example.com',
            'phone': '+48123456789',
            'status': 'lead',
        }

        # Wysyłamy POST request
        response = self.client.post(
            reverse('contacts:contact_create'),
            data=data
        )

        # Sprawdzamy czy został utworzony kontakt
        self.assertEqual(Contact.objects.count(), 1)

        # Sprawdzamy czy dane się zgadzają
        contact = Contact.objects.first()
        self.assertEqual(contact.first_name, 'Nowy')
        self.assertEqual(contact.last_name, 'Kontakt')
        self.assertEqual(contact.email, 'nowy@example.com')
        self.assertEqual(contact.owner, self.user)  # Właściciel to zalogowany user

        # Sprawdzamy przekierowanie (po zapisaniu)
        # 302 = redirect
        self.assertEqual(response.status_code, 302)

    def test_cannot_create_contact_with_duplicate_email(self):
        """
        Test: Nie można utworzyć kontaktu z istniejącym emailem

        Email jest UNIQUE w modelu
        """
        # Tworzymy pierwszy kontakt
        Contact.objects.create(
            first_name='Pierwszy',
            last_name='Kontakt',
            email='test@example.com',
            owner=self.user
        )

        self.client.login(username='testuser', password='testpass123')

        # Próbujemy utworzyć drugi z tym samym emailem
        data = {
            'first_name': 'Drugi',
            'last_name': 'Kontakt',
            'email': 'test@example.com',  # Ten sam email!
            'status': 'lead',
        }

        response = self.client.post(
            reverse('contacts:contact_create'),
            data=data
        )

        # Powinien być tylko JEDEN kontakt (pierwszy)
        self.assertEqual(Contact.objects.count(), 1)

        # Formularz powinien zwrócić błąd (status 200 = formularz z błędami)
        self.assertEqual(response.status_code, 200)

        # Sprawdzamy czy formularz ma błędy
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class TestContactUpdateView(TestCase):
    """
    Testy dla edycji kontaktu
    """

    def setUp(self):
        """Przygotowanie"""
        self.client = Client()

        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        self.contact = Contact.objects.create(
            first_name='Jan',
            last_name='Kowalski',
            email='jan@example.com',
            owner=self.user
        )

    def test_can_update_own_contact(self):
        """
        Test: Edycja własnego kontaktu
        """
        self.client.login(username='testuser', password='testpass123')

        # Nowe dane
        data = {
            'first_name': 'Janusz',  # Zmiana imienia
            'last_name': 'Kowalski',
            'email': 'jan@example.com',
            'status': 'customer',  # Zmiana statusu
        }

        response = self.client.post(
            reverse('contacts:contact_update', args=[self.contact.pk]),
            data=data
        )

        # Odświeżamy kontakt z bazy
        self.contact.refresh_from_db()

        # Sprawdzamy zmiany
        self.assertEqual(self.contact.first_name, 'Janusz')
        self.assertEqual(self.contact.status, 'customer')


class TestContactDeleteView(TestCase):
    """
    Testy dla usuwania kontaktu
    """

    def setUp(self):
        """Przygotowanie"""
        self.client = Client()

        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        self.contact = Contact.objects.create(
            first_name='Do',
            last_name='Usunięcia',
            email='delete@example.com',
            owner=self.user
        )

    def test_can_delete_own_contact(self):
        """
        Test: Usuwanie własnego kontaktu
        """
        self.client.login(username='testuser', password='testpass123')

        # Na początku 1 kontakt
        self.assertEqual(Contact.objects.count(), 1)

        # Wysyłamy POST do delete view
        response = self.client.post(
            reverse('contacts:contact_delete', args=[self.contact.pk])
        )

        # Teraz powinno być 0 kontaktów
        self.assertEqual(Contact.objects.count(), 0)

        # Sprawdzamy przekierowanie
        self.assertEqual(response.status_code, 302)


# PODSUMOWANIE CO SIĘ NAUCZYŁEŚ:
# 1. Client - symuluje przeglądarkę, wysyła requesty
# 2. reverse() - tworzy URL z nazwy (np. 'contacts:contact_list')
# 3. self.client.get() - request GET
# 4. self.client.post() - request POST (formularze)
# 5. self.client.login() - logowanie testowe
# 6. response.status_code - kod HTTP (200, 302, 404, etc.)
# 7. response.context - dane przekazane do szablonu
# 8. assertTemplateUsed() - sprawdza użyty szablon
# 9. assertFormError() - sprawdza błędy formularza
# 10. refresh_from_db() - odświeża obiekt z bazy
# 11. Testowanie autentykacji i uprawnień
# 12. Testowanie izolacji danych między użytkownikami
