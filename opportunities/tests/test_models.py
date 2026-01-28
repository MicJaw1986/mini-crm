"""
Testy modelu Opportunity

CZYTAJ KOMENTARZE - Uczysz się testować modele Django!
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from opportunities.models import Opportunity
from contacts.models import Contact, Company


class OpportunityModelTest(TestCase):
    """
    Testy dla modelu Opportunity

    Co testujemy?
    - Tworzenie opportunity
    - Metody modelu (get_weighted_value, is_won, is_lost, is_overdue)
    - Metody helper (get_stage_color, days_until_close)
    - Metoda move_to_stage
    """

    def setUp(self):
        """
        Przygotowanie danych przed każdym testem

        Tworzymy:
        - Użytkownika testowego
        - Kontakt testowy
        - Firma testowa
        - Opportunity testowa
        """
        # Użytkownik
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        # Kontakt
        self.contact = Contact.objects.create(
            first_name='Jan',
            last_name='Kowalski',
            email='jan@example.com',
            owner=self.user
        )

        # Firma
        self.company = Company.objects.create(
            name='Test Company',
            owner=self.user
        )

        # Opportunity
        self.opportunity = Opportunity.objects.create(
            name='Test Deal',
            description='Test description',
            amount=100000,
            probability=50,
            stage='qualification',
            expected_close_date=timezone.now().date() + timedelta(days=30),
            contact=self.contact,
            company=self.company,
            owner=self.user
        )

    def test_opportunity_creation(self):
        """Test czy opportunity została utworzona poprawnie"""
        self.assertEqual(self.opportunity.name, 'Test Deal')
        self.assertEqual(self.opportunity.amount, 100000)
        self.assertEqual(self.opportunity.probability, 50)
        self.assertEqual(self.opportunity.stage, 'qualification')
        self.assertEqual(self.opportunity.owner, self.user)

    def test_opportunity_str_method(self):
        """Test metody __str__"""
        expected = "Test Deal - Kwalifikacja"
        self.assertEqual(str(self.opportunity), expected)

    def test_get_weighted_value(self):
        """
        Test wartości ważonej (weighted value)

        Wzór: amount * probability / 100
        100,000 * 50% = 50,000
        """
        weighted = self.opportunity.get_weighted_value()
        expected = 100000 * 0.5
        self.assertEqual(weighted, expected)

    def test_get_weighted_value_for_won(self):
        """
        Test wartości ważonej dla wygranej szansy

        Dla closed_won - wartość ważona = pełna wartość (100%)
        """
        self.opportunity.stage = 'closed_won'
        self.opportunity.save()

        weighted = self.opportunity.get_weighted_value()
        self.assertEqual(weighted, self.opportunity.amount)

    def test_get_weighted_value_for_lost(self):
        """
        Test wartości ważonej dla przegranej szansy

        Dla closed_lost - wartość ważona = 0
        """
        self.opportunity.stage = 'closed_lost'
        self.opportunity.save()

        weighted = self.opportunity.get_weighted_value()
        self.assertEqual(weighted, 0)

    def test_is_won_method(self):
        """Test metody is_won()"""
        # Początkowo nie wygrana
        self.assertFalse(self.opportunity.is_won())

        # Przesuń do closed_won
        self.opportunity.stage = 'closed_won'
        self.opportunity.save()

        # Teraz powinna być wygrana
        self.assertTrue(self.opportunity.is_won())

    def test_is_lost_method(self):
        """Test metody is_lost()"""
        # Początkowo nie przegrana
        self.assertFalse(self.opportunity.is_lost())

        # Przesuń do closed_lost
        self.opportunity.stage = 'closed_lost'
        self.opportunity.save()

        # Teraz powinna być przegrana
        self.assertTrue(self.opportunity.is_lost())

    def test_is_open_method(self):
        """Test metody is_open()"""
        # Qualification - otwarta
        self.assertTrue(self.opportunity.is_open())

        # Proposal - otwarta
        self.opportunity.stage = 'proposal'
        self.assertTrue(self.opportunity.is_open())

        # Closed won - zamknięta
        self.opportunity.stage = 'closed_won'
        self.assertFalse(self.opportunity.is_open())

        # Closed lost - zamknięta
        self.opportunity.stage = 'closed_lost'
        self.assertFalse(self.opportunity.is_open())

    def test_is_overdue_for_future_date(self):
        """
        Test czy is_overdue() zwraca False dla przyszłej daty

        Opportunity z expected_close_date za 30 dni
        """
        self.assertFalse(self.opportunity.is_overdue())

    def test_is_overdue_for_past_date(self):
        """
        Test czy is_overdue() zwraca True dla przeszłej daty

        Opportunity z expected_close_date 10 dni temu
        """
        self.opportunity.expected_close_date = timezone.now().date() - timedelta(days=10)
        self.opportunity.save()

        self.assertTrue(self.opportunity.is_overdue())

    def test_is_overdue_for_closed_opportunity(self):
        """
        Test czy is_overdue() zwraca False dla zamkniętej szansy

        Nawet jeśli data była w przeszłości, zamknięta szansa nie jest overdue
        """
        self.opportunity.expected_close_date = timezone.now().date() - timedelta(days=10)
        self.opportunity.stage = 'closed_won'
        self.opportunity.save()

        self.assertFalse(self.opportunity.is_overdue())

    def test_days_until_close(self):
        """
        Test obliczania dni do zamknięcia

        Opportunity z expected_close_date za 30 dni
        """
        days = self.opportunity.days_until_close()
        # Powinno być około 30 dni (może być 29-30 ze względu na timing)
        self.assertGreater(days, 25)
        self.assertLess(days, 35)

    def test_days_until_close_negative(self):
        """
        Test obliczania dni do zamknięcia dla przeterminowanej

        Opportunity z expected_close_date 10 dni temu
        """
        self.opportunity.expected_close_date = timezone.now().date() - timedelta(days=10)
        self.opportunity.save()

        days = self.opportunity.days_until_close()
        # Powinno być około -10 dni
        self.assertLess(days, -5)
        self.assertGreater(days, -15)

    def test_get_stage_color(self):
        """Test metody get_stage_color()"""
        colors = {
            'qualification': 'secondary',
            'proposal': 'info',
            'negotiation': 'warning',
            'closed_won': 'success',
            'closed_lost': 'danger',
        }

        for stage, expected_color in colors.items():
            self.opportunity.stage = stage
            self.assertEqual(self.opportunity.get_stage_color(), expected_color)

    def test_get_probability_color(self):
        """Test metody get_probability_color()"""
        # Prawdopodobieństwo >= 75% -> success
        self.opportunity.probability = 80
        self.assertEqual(self.opportunity.get_probability_color(), 'success')

        # Prawdopodobieństwo >= 50% -> info
        self.opportunity.probability = 60
        self.assertEqual(self.opportunity.get_probability_color(), 'info')

        # Prawdopodobieństwo >= 25% -> warning
        self.opportunity.probability = 40
        self.assertEqual(self.opportunity.get_probability_color(), 'warning')

        # Prawdopodobieństwo < 25% -> danger
        self.opportunity.probability = 20
        self.assertEqual(self.opportunity.get_probability_color(), 'danger')

    def test_move_to_stage_won(self):
        """
        Test przesunięcia do stage closed_won

        Powinno:
        - Ustawić actual_close_date
        - Ustawić probability = 100
        """
        self.opportunity.move_to_stage('closed_won')

        # Odśwież z bazy danych
        self.opportunity.refresh_from_db()

        self.assertEqual(self.opportunity.stage, 'closed_won')
        self.assertEqual(self.opportunity.probability, 100)
        self.assertIsNotNone(self.opportunity.actual_close_date)
        self.assertEqual(self.opportunity.actual_close_date, timezone.now().date())

    def test_move_to_stage_lost(self):
        """
        Test przesunięcia do stage closed_lost

        Powinno:
        - Ustawić actual_close_date
        - Ustawić probability = 0
        """
        self.opportunity.move_to_stage('closed_lost')

        # Odśwież z bazy danych
        self.opportunity.refresh_from_db()

        self.assertEqual(self.opportunity.stage, 'closed_lost')
        self.assertEqual(self.opportunity.probability, 0)
        self.assertIsNotNone(self.opportunity.actual_close_date)

    def test_opportunity_without_contact_and_company(self):
        """
        Test czy opportunity może istnieć bez contact i company

        Contact i company są opcjonalne
        """
        opp = Opportunity.objects.create(
            name='Deal bez kontaktu',
            amount=50000,
            probability=30,
            stage='qualification',
            expected_close_date=timezone.now().date() + timedelta(days=14),
            owner=self.user
        )

        self.assertIsNone(opp.contact)
        self.assertIsNone(opp.company)
        self.assertEqual(opp.owner, self.user)


# PODSUMOWANIE - Co się nauczyłeś:
# 1. setUp() - przygotowanie danych przed testami
# 2. Test tworzenia obiektów
# 3. Test metod modelu (business logic)
# 4. Test metod helper (UI helpers)
# 5. Test danych opcjonalnych (null=True, blank=True)
# 6. refresh_from_db() - odświeżenie obiektu z bazy
# 7. Testy dat i timezone
# 8. Testy logiki warunkowej (if/else w metodach)
