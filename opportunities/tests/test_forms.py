"""
Testy formularzy Opportunity

CZYTAJ KOMENTARZE - Walidacja formularzy!
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from opportunities.forms import OpportunityForm
from contacts.models import Contact, Company


class OpportunityFormTest(TestCase):
    """
    Testy dla OpportunityForm

    Co testujemy?
    - Walidacja pól
    - Wymagane pola
    - Queryset filtering (bezpieczeństwo)
    - Custom validation (clean methods)
    """

    def setUp(self):
        """Przygotowanie danych testowych"""
        # Użytkownik 1
        self.user1 = User.objects.create_user(
            username='user1',
            password='pass123'
        )

        # Użytkownik 2
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

        # Kontakt i firma dla user2
        self.contact2 = Contact.objects.create(
            first_name='Anna',
            last_name='Nowak',
            email='anna@example.com',
            owner=self.user2
        )

        self.company2 = Company.objects.create(
            name='Company 2',
            owner=self.user2
        )

    def test_valid_form(self):
        """Test czy prawidłowy formularz przechodzi walidację"""
        data = {
            'name': 'Test Deal',
            'description': 'Test description',
            'amount': 100000,
            'probability': 50,
            'stage': 'qualification',
            'expected_close_date': (timezone.now().date() + timedelta(days=30)).isoformat(),
        }

        form = OpportunityForm(data=data, user=self.user1)
        self.assertTrue(form.is_valid())

    def test_name_required(self):
        """Test czy pole name jest wymagane"""
        data = {
            # Brak name
            'amount': 100000,
            'probability': 50,
            'stage': 'qualification',
            'expected_close_date': (timezone.now().date() + timedelta(days=30)).isoformat(),
        }

        form = OpportunityForm(data=data, user=self.user1)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_amount_required(self):
        """Test czy pole amount jest wymagane"""
        data = {
            'name': 'Test Deal',
            # Brak amount
            'probability': 50,
            'stage': 'qualification',
            'expected_close_date': (timezone.now().date() + timedelta(days=30)).isoformat(),
        }

        form = OpportunityForm(data=data, user=self.user1)
        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)

    def test_probability_required(self):
        """Test czy pole probability jest wymagane"""
        data = {
            'name': 'Test Deal',
            'amount': 100000,
            # Brak probability
            'stage': 'qualification',
            'expected_close_date': (timezone.now().date() + timedelta(days=30)).isoformat(),
        }

        form = OpportunityForm(data=data, user=self.user1)
        self.assertFalse(form.is_valid())
        self.assertIn('probability', form.errors)

    def test_expected_close_date_required(self):
        """Test czy pole expected_close_date jest wymagane"""
        data = {
            'name': 'Test Deal',
            'amount': 100000,
            'probability': 50,
            'stage': 'qualification',
            # Brak expected_close_date
        }

        form = OpportunityForm(data=data, user=self.user1)
        self.assertFalse(form.is_valid())
        self.assertIn('expected_close_date', form.errors)

    def test_description_not_required(self):
        """Test czy pole description jest opcjonalne"""
        data = {
            'name': 'Test Deal',
            # Brak description - OK
            'amount': 100000,
            'probability': 50,
            'stage': 'qualification',
            'expected_close_date': (timezone.now().date() + timedelta(days=30)).isoformat(),
        }

        form = OpportunityForm(data=data, user=self.user1)
        self.assertTrue(form.is_valid())

    def test_contact_not_required(self):
        """Test czy pole contact jest opcjonalne"""
        data = {
            'name': 'Test Deal',
            'amount': 100000,
            'probability': 50,
            'stage': 'qualification',
            'expected_close_date': (timezone.now().date() + timedelta(days=30)).isoformat(),
            # Brak contact - OK
        }

        form = OpportunityForm(data=data, user=self.user1)
        self.assertTrue(form.is_valid())

    def test_probability_validation_too_high(self):
        """
        Test walidacji probability - za wysokie (>100)

        clean_probability() powinno zwrócić błąd
        """
        data = {
            'name': 'Test Deal',
            'amount': 100000,
            'probability': 150,  # Za wysokie!
            'stage': 'qualification',
            'expected_close_date': (timezone.now().date() + timedelta(days=30)).isoformat(),
        }

        form = OpportunityForm(data=data, user=self.user1)
        self.assertFalse(form.is_valid())
        self.assertIn('probability', form.errors)

    def test_probability_validation_too_low(self):
        """
        Test walidacji probability - za niskie (<0)

        clean_probability() powinno zwrócić błąd
        """
        data = {
            'name': 'Test Deal',
            'amount': 100000,
            'probability': -10,  # Za niskie!
            'stage': 'qualification',
            'expected_close_date': (timezone.now().date() + timedelta(days=30)).isoformat(),
        }

        form = OpportunityForm(data=data, user=self.user1)
        self.assertFalse(form.is_valid())
        self.assertIn('probability', form.errors)

    def test_contact_queryset_filtered_by_user(self):
        """
        Test czy queryset contact jest filtrowany po użytkowniku

        BEZPIECZEŃSTWO! Użytkownik widzi tylko swoje kontakty
        """
        form = OpportunityForm(user=self.user1)

        contact_queryset = form.fields['contact'].queryset

        # User1 widzi tylko swój kontakt
        self.assertIn(self.contact1, contact_queryset)
        self.assertNotIn(self.contact2, contact_queryset)

    def test_company_queryset_filtered_by_user(self):
        """
        Test czy queryset company jest filtrowany po użytkowniku

        BEZPIECZEŃSTWO! Użytkownik widzi tylko swoje firmy
        """
        form = OpportunityForm(user=self.user2)

        company_queryset = form.fields['company'].queryset

        # User2 widzi tylko swoją firmę
        self.assertIn(self.company2, company_queryset)
        self.assertNotIn(self.company1, company_queryset)

    def test_closed_lost_requires_lost_reason(self):
        """
        Test walidacji - jeśli stage=closed_lost, wymagany lost_reason

        clean() powinno zwrócić błąd
        """
        data = {
            'name': 'Test Deal',
            'amount': 100000,
            'probability': 50,
            'stage': 'closed_lost',  # Przegrana
            'expected_close_date': (timezone.now().date() + timedelta(days=30)).isoformat(),
            # Brak lost_reason - błąd!
        }

        form = OpportunityForm(data=data, user=self.user1)
        self.assertFalse(form.is_valid())
        self.assertIn('lost_reason', form.errors)

    def test_closed_won_requires_actual_close_date(self):
        """
        Test walidacji - jeśli stage=closed_won, wymagane actual_close_date

        clean() powinno zwrócić błąd
        """
        data = {
            'name': 'Test Deal',
            'amount': 100000,
            'probability': 50,
            'stage': 'closed_won',  # Wygrana
            'expected_close_date': (timezone.now().date() + timedelta(days=30)).isoformat(),
            # Brak actual_close_date - błąd!
        }

        form = OpportunityForm(data=data, user=self.user1)
        self.assertFalse(form.is_valid())
        self.assertIn('actual_close_date', form.errors)

    def test_closed_lost_requires_actual_close_date(self):
        """
        Test walidacji - jeśli stage=closed_lost, wymagane actual_close_date

        clean() powinno zwrócić błąd
        """
        data = {
            'name': 'Test Deal',
            'amount': 100000,
            'probability': 50,
            'stage': 'closed_lost',  # Przegrana
            'expected_close_date': (timezone.now().date() + timedelta(days=30)).isoformat(),
            'lost_reason': 'price',  # OK
            # Brak actual_close_date - błąd!
        }

        form = OpportunityForm(data=data, user=self.user1)
        self.assertFalse(form.is_valid())
        self.assertIn('actual_close_date', form.errors)

    def test_closed_won_with_actual_close_date_valid(self):
        """Test czy closed_won z actual_close_date przechodzi walidację"""
        data = {
            'name': 'Test Deal',
            'amount': 100000,
            'probability': 50,
            'stage': 'closed_won',
            'expected_close_date': (timezone.now().date() + timedelta(days=30)).isoformat(),
            'actual_close_date': timezone.now().date().isoformat(),  # OK
        }

        form = OpportunityForm(data=data, user=self.user1)
        self.assertTrue(form.is_valid())

    def test_open_stage_does_not_require_actual_close_date(self):
        """Test czy otwarte stage nie wymagają actual_close_date"""
        for stage in ['qualification', 'proposal', 'negotiation']:
            data = {
                'name': 'Test Deal',
                'amount': 100000,
                'probability': 50,
                'stage': stage,
                'expected_close_date': (timezone.now().date() + timedelta(days=30)).isoformat(),
                # Brak actual_close_date - OK dla otwartych
            }

            form = OpportunityForm(data=data, user=self.user1)
            self.assertTrue(form.is_valid(), f"Stage {stage} should be valid without actual_close_date")


# PODSUMOWANIE - Co się nauczyłeś:
# 1. Test walidacji formularza (is_valid())
# 2. Test wymaganych pól (required=True)
# 3. Test opcjonalnych pól (required=False)
# 4. Test custom validation (clean_probability, clean)
# 5. Test filtrowania querysetów (bezpieczeństwo!)
# 6. Test logiki biznesowej w formularzach
# 7. assertIn('field', form.errors) - sprawdzanie błędów
# 8. Testowanie wielu scenariuszy w pętli
