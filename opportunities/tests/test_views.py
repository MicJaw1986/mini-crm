"""
Testy widoków Opportunity

CZYTAJ KOMENTARZE - Pełne testy CRUD + bezpieczeństwo!
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from opportunities.models import Opportunity
from contacts.models import Contact, Company


class OpportunityViewsTest(TestCase):
    """
    Testy widoków dla Opportunity

    Co testujemy?
    - Autentykacja (@login_required)
    - Izolacja danych (data isolation)
    - CRUD operations (list, detail, create, update, delete)
    - Wyszukiwanie i filtrowanie
    - Move stage action
    """

    def setUp(self):
        """Przygotowanie danych testowych"""
        # Client do symulacji przeglądarki
        self.client = Client()

        # Pierwszy użytkownik
        self.user1 = User.objects.create_user(
            username='user1',
            password='pass123'
        )

        # Drugi użytkownik (do testowania izolacji)
        self.user2 = User.objects.create_user(
            username='user2',
            password='pass123'
        )

        # Kontakt i firma dla user1
        self.contact1 = Contact.objects.create(
            first_name='Jan',
            last_name='Kowalski',
            email='jan@example.com',
            owner=self.user1
        )

        self.company1 = Company.objects.create(
            name='Company 1',
            owner=self.user1
        )

        # Opportunity dla user1
        self.opp1 = Opportunity.objects.create(
            name='Deal 1',
            amount=100000,
            probability=50,
            stage='qualification',
            expected_close_date=timezone.now().date() + timedelta(days=30),
            contact=self.contact1,
            company=self.company1,
            owner=self.user1
        )

        # Opportunity dla user2 (do testowania izolacji)
        self.opp2 = Opportunity.objects.create(
            name='Deal 2',
            amount=50000,
            probability=30,
            stage='proposal',
            expected_close_date=timezone.now().date() + timedelta(days=15),
            owner=self.user2
        )

    def test_list_view_redirect_if_not_logged_in(self):
        """
        Test czy niezalogowany użytkownik jest przekierowany

        BEZPIECZEŃSTWO: Wymuszamy logowanie
        """
        response = self.client.get(reverse('opportunities:opportunity_list'))

        # 302 = redirect
        self.assertEqual(response.status_code, 302)
        # Sprawdź czy redirect prowadzi do strony logowania
        self.assertIn('/accounts/login/', response.url)

    def test_list_view_accessible_for_logged_in_user(self):
        """Test czy zalogowany użytkownik może zobaczyć listę"""
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('opportunities:opportunity_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'opportunities/opportunity_list.html')

    def test_list_view_shows_only_user_opportunities(self):
        """
        Test izolacji danych - DATA ISOLATION

        KLUCZOWE DLA BEZPIECZEŃSTWA!
        Użytkownik widzi tylko swoje opportunities
        """
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('opportunities:opportunity_list'))

        opportunities = response.context['opportunities']

        # User1 widzi tylko swoją opportunity
        self.assertIn(self.opp1, opportunities)
        self.assertNotIn(self.opp2, opportunities)
        self.assertEqual(len(opportunities), 1)

    def test_list_view_search(self):
        """Test wyszukiwania"""
        self.client.login(username='user1', password='pass123')

        # Szukaj po nazwie
        response = self.client.get(
            reverse('opportunities:opportunity_list'),
            {'search': 'Deal 1'}
        )

        opportunities = response.context['opportunities']
        self.assertIn(self.opp1, opportunities)

    def test_list_view_filter_by_stage(self):
        """Test filtrowania po stage"""
        self.client.login(username='user1', password='pass123')

        response = self.client.get(
            reverse('opportunities:opportunity_list'),
            {'stage': 'qualification'}
        )

        opportunities = response.context['opportunities']
        self.assertEqual(len(opportunities), 1)
        self.assertEqual(opportunities[0].stage, 'qualification')

    def test_detail_view_redirect_if_not_logged_in(self):
        """Test przekierowania dla niezalogowanego"""
        response = self.client.get(
            reverse('opportunities:opportunity_detail', args=[self.opp1.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_detail_view_accessible_for_owner(self):
        """Test czy właściciel może zobaczyć szczegóły"""
        self.client.login(username='user1', password='pass123')
        response = self.client.get(
            reverse('opportunities:opportunity_detail', args=[self.opp1.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'opportunities/opportunity_detail.html')
        self.assertEqual(response.context['opportunity'], self.opp1)

    def test_detail_view_not_accessible_for_other_user(self):
        """
        Test izolacji - user2 NIE może zobaczyć opportunity user1

        BEZPIECZEŃSTWO!
        """
        self.client.login(username='user2', password='pass123')
        response = self.client.get(
            reverse('opportunities:opportunity_detail', args=[self.opp1.pk])
        )

        # 404 - nie znaleziono (z punktu widzenia user2)
        self.assertEqual(response.status_code, 404)

    def test_create_view_get(self):
        """Test widoku tworzenia - GET (pokaż formularz)"""
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('opportunities:opportunity_create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'opportunities/opportunity_form.html')
        self.assertIn('form', response.context)

    def test_create_view_post(self):
        """Test widoku tworzenia - POST (zapisz)"""
        self.client.login(username='user1', password='pass123')

        data = {
            'name': 'New Deal',
            'description': 'Test description',
            'amount': 75000,
            'probability': 40,
            'stage': 'proposal',
            'expected_close_date': (timezone.now().date() + timedelta(days=20)).isoformat(),
            'contact': self.contact1.pk,
            'company': self.company1.pk,
        }

        response = self.client.post(
            reverse('opportunities:opportunity_create'),
            data
        )

        # Sprawdź czy opportunity została utworzona
        self.assertEqual(Opportunity.objects.filter(name='New Deal').count(), 1)

        new_opp = Opportunity.objects.get(name='New Deal')

        # Sprawdź czy owner został ustawiony na zalogowanego użytkownika
        self.assertEqual(new_opp.owner, self.user1)

        # Sprawdź przekierowanie do szczegółów
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse('opportunities:opportunity_detail', args=[new_opp.pk])
        )

    def test_create_view_filters_contact_and_company_by_user(self):
        """
        Test czy formularz pokazuje tylko kontakty/firmy użytkownika

        BEZPIECZEŃSTWO!
        """
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('opportunities:opportunity_create'))

        form = response.context['form']

        # Sprawdź querysety formularza
        contact_queryset = form.fields['contact'].queryset
        company_queryset = form.fields['company'].queryset

        # User1 widzi tylko swoje kontakty/firmy
        self.assertIn(self.contact1, contact_queryset)
        self.assertIn(self.company1, company_queryset)

    def test_update_view_get(self):
        """Test widoku edycji - GET"""
        self.client.login(username='user1', password='pass123')
        response = self.client.get(
            reverse('opportunities:opportunity_update', args=[self.opp1.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'opportunities/opportunity_form.html')

        form = response.context['form']
        # Sprawdź czy formularz ma dane opportunity
        self.assertEqual(form.instance, self.opp1)

    def test_update_view_post(self):
        """Test widoku edycji - POST"""
        self.client.login(username='user1', password='pass123')

        data = {
            'name': 'Updated Deal',
            'description': 'Updated description',
            'amount': 120000,
            'probability': 60,
            'stage': 'negotiation',
            'expected_close_date': self.opp1.expected_close_date.isoformat(),
            'contact': self.contact1.pk,
            'company': self.company1.pk,
        }

        response = self.client.post(
            reverse('opportunities:opportunity_update', args=[self.opp1.pk]),
            data
        )

        # Odśwież z bazy
        self.opp1.refresh_from_db()

        # Sprawdź czy dane zostały zaktualizowane
        self.assertEqual(self.opp1.name, 'Updated Deal')
        self.assertEqual(self.opp1.amount, 120000)
        self.assertEqual(self.opp1.stage, 'negotiation')

        # Sprawdź przekierowanie
        self.assertEqual(response.status_code, 302)

    def test_update_view_not_accessible_for_other_user(self):
        """
        Test czy user2 NIE może edytować opportunity user1

        BEZPIECZEŃSTWO!
        """
        self.client.login(username='user2', password='pass123')
        response = self.client.get(
            reverse('opportunities:opportunity_update', args=[self.opp1.pk])
        )

        # 404 - nie znaleziono
        self.assertEqual(response.status_code, 404)

    def test_delete_view_get(self):
        """Test widoku usuwania - GET (pokaż potwierdzenie)"""
        self.client.login(username='user1', password='pass123')
        response = self.client.get(
            reverse('opportunities:opportunity_delete', args=[self.opp1.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'opportunities/opportunity_confirm_delete.html')

    def test_delete_view_post(self):
        """Test widoku usuwania - POST (usuń)"""
        self.client.login(username='user1', password='pass123')

        opp_pk = self.opp1.pk

        response = self.client.post(
            reverse('opportunities:opportunity_delete', args=[opp_pk])
        )

        # Sprawdź czy opportunity została usunięta
        self.assertFalse(Opportunity.objects.filter(pk=opp_pk).exists())

        # Sprawdź przekierowanie do listy
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('opportunities:opportunity_list'))

    def test_delete_view_not_accessible_for_other_user(self):
        """
        Test czy user2 NIE może usunąć opportunity user1

        BEZPIECZEŃSTWO!
        """
        self.client.login(username='user2', password='pass123')
        response = self.client.post(
            reverse('opportunities:opportunity_delete', args=[self.opp1.pk])
        )

        # 404 - nie znaleziono
        self.assertEqual(response.status_code, 404)

        # Opportunity nadal istnieje
        self.assertTrue(Opportunity.objects.filter(pk=self.opp1.pk).exists())

    def test_move_stage_action(self):
        """Test akcji move_stage"""
        self.client.login(username='user1', password='pass123')

        response = self.client.get(
            reverse('opportunities:opportunity_move_stage', args=[self.opp1.pk, 'proposal'])
        )

        # Odśwież z bazy
        self.opp1.refresh_from_db()

        # Sprawdź czy stage został zmieniony
        self.assertEqual(self.opp1.stage, 'proposal')

        # Sprawdź przekierowanie
        self.assertEqual(response.status_code, 302)

    def test_move_stage_invalid_stage(self):
        """Test move_stage z nieprawidłowym stage"""
        self.client.login(username='user1', password='pass123')

        original_stage = self.opp1.stage

        response = self.client.get(
            reverse('opportunities:opportunity_move_stage', args=[self.opp1.pk, 'invalid_stage'])
        )

        # Odśwież z bazy
        self.opp1.refresh_from_db()

        # Stage nie powinien się zmienić
        self.assertEqual(self.opp1.stage, original_stage)

    def test_list_view_statistics(self):
        """Test statystyk na stronie listy"""
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('opportunities:opportunity_list'))

        stats = response.context['stats']

        self.assertEqual(stats['total'], 1)
        self.assertEqual(stats['open'], 1)
        self.assertEqual(stats['won'], 0)
        self.assertEqual(stats['lost'], 0)


# PODSUMOWANIE - Co się nauczyłeś:
# 1. Test autentykacji (@login_required)
# 2. Test izolacji danych (data isolation) - BEZPIECZEŃSTWO!
# 3. Test CRUD operations (GET i POST)
# 4. Test przekierowań (302 status code)
# 5. Test filtrowania querysetów w formularzach
# 6. Test wyszukiwania i filtrowania
# 7. Test custom actions (move_stage)
# 8. Test walidacji (invalid stage)
# 9. Client.login() i Client.get/post()
# 10. assertIn, assertNotIn, assertEqual, assertTrue, assertFalse
