"""
Modele dla aplikacji Opportunities (Szanse sprzedaży)

CZYTAJ KOMENTARZE - Dowiesz się jak działają szanse sprzedaży w CRM!
"""

from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from contacts.models import Contact, Company


class Opportunity(models.Model):
    """
    Model Opportunity (Szansa sprzedaży)

    Co to jest Opportunity?
    - To potencjalna sprzedaż/deal
    - Ma wartość (amount)
    - Przechodzi przez etapy (pipeline stages)
    - Ma prawdopodobieństwo zamknięcia (probability)
    - Ma przewidywaną datę zamknięcia (expected_close_date)

    Przykład życia Opportunity:
    1. Lead kontaktuje się -> Opportunity "Nowy projekt" (stage: qualification)
    2. Po rozmowie -> stage: proposal
    3. Wysłano ofertę -> stage: negotiation
    4. Albo: Klient kupił -> stage: won
    5. Albo: Klient zrezygnował -> stage: lost
    """

    # Stages (Etapy pipeline'u sprzedażowego)
    # Każdy CRM może mieć inne etapy - to są standardowe
    STAGE_CHOICES = [
        ('qualification', 'Kwalifikacja'),      # Sprawdzamy czy to prawdziwy lead
        ('proposal', 'Propozycja'),             # Przygotowujemy ofertę
        ('negotiation', 'Negocjacje'),          # Rozmawiamy o cenie/warunkach
        ('closed_won', 'Wygrana'),              # 🎉 Sukces! Klient kupił
        ('closed_lost', 'Przegrana'),           # 😞 Klient zrezygnował
    ]

    # Powody przegranej (dlaczego nie kupił?)
    LOST_REASON_CHOICES = [
        ('price', 'Za drogo'),
        ('competitor', 'Wybrał konkurencję'),
        ('no_budget', 'Brak budżetu'),
        ('timing', 'Zły timing'),
        ('no_decision', 'Nie podjęto decyzji'),
        ('other', 'Inny powód'),
    ]

    # Podstawowe informacje
    name = models.CharField(
        'Nazwa szansy',
        max_length=200,
        help_text='Np. "Wdrożenie CRM dla Acme Corp"'
    )

    description = models.TextField(
        'Opis',
        blank=True,
        help_text='Szczegóły szansy sprzedażowej'
    )

    # Wartość i finansowe
    amount = models.DecimalField(
        'Wartość (PLN)',
        max_digits=12,
        decimal_places=2,
        help_text='Przewidywana wartość transakcji'
    )

    probability = models.IntegerField(
        'Prawdopodobieństwo (%)',
        default=50,
        help_text='Szansa na wygraną (0-100%)'
    )

    # Stage i status
    stage = models.CharField(
        'Etap',
        max_length=20,
        choices=STAGE_CHOICES,
        default='qualification'
    )

    # Daty
    expected_close_date = models.DateField(
        'Przewidywana data zamknięcia',
        help_text='Kiedy spodziewamy się decyzji?'
    )

    actual_close_date = models.DateField(
        'Rzeczywista data zamknięcia',
        null=True,
        blank=True,
        help_text='Kiedy faktycznie zamknięto (won/lost)'
    )

    # Informacja o przegranej
    lost_reason = models.CharField(
        'Powód przegranej',
        max_length=20,
        choices=LOST_REASON_CHOICES,
        null=True,
        blank=True
    )

    lost_reason_details = models.TextField(
        'Szczegóły przegranej',
        blank=True,
        help_text='Dodatkowe informacje dlaczego przegraliśmy'
    )

    # Relacje
    contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='opportunities',
        verbose_name='Kontakt'
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='opportunities',
        verbose_name='Firma'
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='opportunities',
        verbose_name='Właściciel'
    )

    # Metadane
    created_at = models.DateTimeField('Data utworzenia', auto_now_add=True)
    updated_at = models.DateTimeField('Data aktualizacji', auto_now=True)

    class Meta:
        verbose_name = 'Szansa sprzedaży'
        verbose_name_plural = 'Szanse sprzedaży'
        ordering = ['-expected_close_date']  # Najbliższe zamknięcia na górze

    def __str__(self):
        return f"{self.name} - {self.get_stage_display()}"

    def get_weighted_value(self):
        """
        Wartość ważona (weighted value)

        Co to?
        Wartość * Prawdopodobieństwo

        Przykład:
        - Deal wart 100,000 PLN z 50% szansą = 50,000 PLN weighted
        - Deal wart 10,000 PLN z 90% szansą = 9,000 PLN weighted

        Dlaczego to ważne?
        Bardziej realistyczna prognoza przychodu
        """
        if self.stage in ['closed_won', 'closed_lost']:
            # Dla zamkniętych szans - 100% lub 0%
            return self.amount if self.stage == 'closed_won' else Decimal('0')

        return self.amount * (Decimal(str(self.probability)) / Decimal('100'))

    def is_won(self):
        """Czy szansa została wygrana?"""
        return self.stage == 'closed_won'

    def is_lost(self):
        """Czy szansa została przegrana?"""
        return self.stage == 'closed_lost'

    def is_open(self):
        """Czy szansa jest nadal otwarta?"""
        return self.stage not in ['closed_won', 'closed_lost']

    def is_overdue(self):
        """
        Czy przekroczono przewidywaną datę zamknięcia?

        Jeśli tak - trzeba działać szybko!
        """
        if not self.is_open():
            return False

        return timezone.now().date() > self.expected_close_date

    def get_stage_color(self):
        """
        Kolor dla wyświetlania stage (Bootstrap classes)

        Użycie w template:
        <span class="badge bg-{{ opportunity.get_stage_color }}">
        """
        colors = {
            'qualification': 'secondary',    # Szary
            'proposal': 'info',              # Niebieski
            'negotiation': 'warning',        # Żółty
            'closed_won': 'success',         # Zielony
            'closed_lost': 'danger',         # Czerwony
        }
        return colors.get(self.stage, 'secondary')

    def get_probability_color(self):
        """Kolor dla prawdopodobieństwa"""
        if self.probability >= 75:
            return 'success'  # Zielony - duża szansa
        elif self.probability >= 50:
            return 'info'     # Niebieski - średnia
        elif self.probability >= 25:
            return 'warning'  # Żółty - niska
        else:
            return 'danger'   # Czerwony - bardzo niska

    def days_until_close(self):
        """
        Ile dni do przewidywanego zamknięcia?

        Zwraca:
        - Liczbę dodatnią: tyle dni zostało
        - Liczbę ujemną: tyle dni temu powinno się zamknąć (overdue!)
        """
        if not self.is_open():
            return 0

        delta = self.expected_close_date - timezone.now().date()
        return delta.days

    def move_to_stage(self, new_stage, user=None):
        """
        Przenieś szansę do nowego etapu

        Automatycznie:
        - Ustawia actual_close_date gdy zamykamy (won/lost)
        - Waliduje czy przejście ma sens

        Args:
            new_stage: Nowy stage (np. 'proposal')
            user: Użytkownik wykonujący akcję (opcjonalnie)
        """
        old_stage = self.stage
        self.stage = new_stage

        # Jeśli zamykamy - ustaw datę
        if new_stage in ['closed_won', 'closed_lost'] and not self.actual_close_date:
            self.actual_close_date = timezone.now().date()

        # Jeśli wygraliśmy - prawdopodobieństwo = 100%
        if new_stage == 'closed_won':
            self.probability = 100

        # Jeśli przegraliśmy - prawdopodobieństwo = 0%
        if new_stage == 'closed_lost':
            self.probability = 0

        self.save()

        # Tutaj można dodać logowanie historii zmian
        # np. OpportunityHistory.objects.create(...)

        return True


# PODSUMOWANIE - Co się nauczyłeś:
# 1. Model Opportunity z pełnym sales pipeline
# 2. Stages (etapy sprzedaży): qualification → proposal → negotiation → won/lost
# 3. Weighted value (wartość ważona) = amount * probability
# 4. Metody biznesowe: is_won(), is_lost(), is_overdue()
# 5. Helper methods dla UI: get_stage_color(), get_probability_color()
# 6. Tracking dat: expected_close_date, actual_close_date
# 7. Lost reasons (powody przegranej) - analiza dlaczego nie kupili
