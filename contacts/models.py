from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Company(models.Model):
    """Model reprezentujący firmę"""

    name = models.CharField('Nazwa firmy', max_length=200)
    nip = models.CharField(
        'NIP',
        max_length=10,
        blank=True,
        validators=[RegexValidator(regex=r'^\d{10}$', message='NIP musi składać się z 10 cyfr')]
    )
    industry = models.CharField('Branża', max_length=100, blank=True)
    website = models.URLField('Strona WWW', blank=True)
    phone = models.CharField('Telefon', max_length=20, blank=True)
    email = models.EmailField('Email', blank=True)

    # Adres
    street = models.CharField('Ulica', max_length=200, blank=True)
    city = models.CharField('Miasto', max_length=100, blank=True)
    postal_code = models.CharField('Kod pocztowy', max_length=10, blank=True)
    country = models.CharField('Kraj', max_length=100, default='Polska')

    # Integracja z ERP
    erp_customer_code = models.CharField(
        'Kod kontrahenta w ERP',
        max_length=50,
        blank=True,
        help_text='Kod klienta w systemie ERP (np. Comarch XL)'
    )

    # Metadata
    notes = models.TextField('Notatki', blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Właściciel', related_name='companies')
    created_at = models.DateTimeField('Data utworzenia', auto_now_add=True)
    updated_at = models.DateTimeField('Data aktualizacji', auto_now=True)

    class Meta:
        verbose_name = 'Firma'
        verbose_name_plural = 'Firmy'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_full_address(self):
        """Zwraca pełny adres firmy"""
        parts = [self.street, f"{self.postal_code} {self.city}", self.country]
        return ', '.join(filter(None, parts))


class Contact(models.Model):
    """Model reprezentujący kontakt (osobę)"""

    STATUS_CHOICES = [
        ('lead', 'Lead'),
        ('prospect', 'Prospect'),
        ('customer', 'Klient'),
        ('churned', 'Utracony'),
    ]

    # Dane podstawowe
    first_name = models.CharField('Imię', max_length=100)
    last_name = models.CharField('Nazwisko', max_length=100)
    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Telefon', max_length=20, blank=True)
    mobile = models.CharField('Telefon komórkowy', max_length=20, blank=True)

    # Powiązania
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Firma',
        related_name='contacts'
    )
    position = models.CharField('Stanowisko', max_length=100, blank=True)

    # Status i kategoria
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='lead')
    tags = models.CharField('Tagi', max_length=200, blank=True, help_text='Oddziel przecinkami')

    # Adres (jeśli inny niż firma)
    street = models.CharField('Ulica', max_length=200, blank=True)
    city = models.CharField('Miasto', max_length=100, blank=True)
    postal_code = models.CharField('Kod pocztowy', max_length=10, blank=True)
    country = models.CharField('Kraj', max_length=100, blank=True)

    # Metadata
    notes = models.TextField('Notatki', blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Właściciel', related_name='contacts')
    created_at = models.DateTimeField('Data utworzenia', auto_now_add=True)
    updated_at = models.DateTimeField('Data aktualizacji', auto_now=True)
    last_contact_date = models.DateField('Data ostatniego kontaktu', null=True, blank=True)

    class Meta:
        verbose_name = 'Kontakt'
        verbose_name_plural = 'Kontakty'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        """Zwraca pełne imię i nazwisko"""
        return f"{self.first_name} {self.last_name}"

    def get_full_address(self):
        """Zwraca pełny adres kontaktu"""
        if self.company and not any([self.street, self.city, self.postal_code]):
            return self.company.get_full_address()
        parts = [self.street, f"{self.postal_code} {self.city}", self.country]
        return ', '.join(filter(None, parts))

    def get_tags_list(self):
        """Zwraca listę tagów"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
