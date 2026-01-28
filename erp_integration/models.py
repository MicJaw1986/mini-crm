"""
Modele do cache'owania danych z ERP

INSTRUKCJA:
1. Te modele przechowują KOPIĘ danych z ERP w Django
2. Odświeżane są przez task synchronizacji (opcjonalnie)
3. Umożliwiają szybkie zapytania bez ciągłego odpytywania API ERP
4. Można używać bez cache - wtedy zawsze live data z API
"""

from django.db import models
from django.contrib.auth.models import User
from contacts.models import Company


class ERPSyncLog(models.Model):
    """
    Log synchronizacji z ERP

    Śledzi kiedy i co było synchronizowane
    """
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='erp_sync_logs',
        null=True,
        blank=True,
        help_text="Firma której dotyczy synchronizacja"
    )
    sync_type = models.CharField(
        max_length=50,
        choices=[
            ('orders', 'Zamówienia'),
            ('invoices', 'Faktury'),
            ('delivery_notes', 'Dokumenty WZ'),
            ('payments', 'Płatności'),
            ('summary', 'Podsumowanie'),
            ('full', 'Pełna synchronizacja'),
        ],
        help_text="Typ synchronizacji"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('success', 'Sukces'),
            ('error', 'Błąd'),
            ('partial', 'Częściowy'),
        ],
        default='success'
    )
    records_synced = models.IntegerField(
        default=0,
        help_text="Liczba zsynchronizowanych rekordów"
    )
    error_message = models.TextField(
        blank=True,
        help_text="Komunikat błędu (jeśli wystąpił)"
    )
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.FloatField(
        null=True,
        blank=True,
        help_text="Czas trwania synchronizacji w sekundach"
    )

    class Meta:
        ordering = ['-started_at']
        verbose_name = "Log synchronizacji ERP"
        verbose_name_plural = "Logi synchronizacji ERP"

    def __str__(self):
        return f"{self.sync_type} - {self.status} ({self.started_at})"


class ERPCustomerCache(models.Model):
    """
    Cache danych kontrahenta z ERP

    Opcjonalny - jeśli chcesz cache'ować dane klienta
    """
    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name='erp_cache',
        help_text="Powiązana firma w CRM"
    )
    customer_code = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        help_text="Kod kontrahenta w ERP"
    )

    # Dane z ERP (cache)
    name = models.CharField(max_length=200, blank=True)
    nip = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    payment_terms = models.CharField(max_length=100, blank=True)
    credit_limit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        help_text="Limit kredytowy"
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        help_text="Saldo (dodatnie = nasz dług, ujemne = ich dług)"
    )

    # Metadane cache
    last_synced = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cache kontrahenta ERP"
        verbose_name_plural = "Cache kontrahentów ERP"

    def __str__(self):
        return f"{self.customer_code} - {self.name}"


class ERPOrder(models.Model):
    """
    Cache zamówień z ERP

    Opcjonalny - możesz cache'ować zamówienia lub zawsze pobierać live
    """
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='erp_orders',
        help_text="Firma której dotyczy zamówienie"
    )
    order_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="ID zamówienia w ERP"
    )
    order_number = models.CharField(max_length=100)
    order_date = models.DateField()

    total_net = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_gross = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='PLN')

    status = models.CharField(
        max_length=50,
        choices=[
            ('draft', 'Projekt'),
            ('confirmed', 'Potwierdzony'),
            ('in_progress', 'W realizacji'),
            ('completed', 'Zrealizowany'),
            ('cancelled', 'Anulowany'),
        ],
        default='draft'
    )

    delivery_date = models.DateField(null=True, blank=True)

    # Raw data from ERP (JSON)
    raw_data = models.JSONField(
        null=True,
        blank=True,
        help_text="Pełne dane z API ERP (backup)"
    )

    last_synced = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-order_date']
        verbose_name = "Zamówienie ERP"
        verbose_name_plural = "Zamówienia ERP"

    def __str__(self):
        return f"{self.order_number} - {self.company.name}"


class ERPInvoice(models.Model):
    """
    Cache faktur z ERP
    """
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='erp_invoices',
        help_text="Firma której dotyczy faktura"
    )
    invoice_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="ID faktury w ERP"
    )
    invoice_number = models.CharField(max_length=100)
    invoice_type = models.CharField(
        max_length=10,
        choices=[
            ('FS', 'Faktura sprzedaży'),
            ('FKOR', 'Faktura korygująca'),
            ('FP', 'Faktura pro-forma'),
            ('FV', 'Faktura VAT'),
        ],
        default='FS'
    )

    invoice_date = models.DateField()
    sale_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    total_net = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_gross = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='PLN')

    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('paid', 'Opłacona'),
            ('unpaid', 'Nieopłacona'),
            ('overdue', 'Zaległa'),
            ('partial', 'Częściowo opłacona'),
        ],
        default='unpaid'
    )

    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    remaining_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Raw data from ERP (JSON)
    raw_data = models.JSONField(
        null=True,
        blank=True,
        help_text="Pełne dane z API ERP"
    )

    last_synced = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-invoice_date']
        verbose_name = "Faktura ERP"
        verbose_name_plural = "Faktury ERP"

    def __str__(self):
        return f"{self.invoice_number} - {self.company.name}"

    def is_overdue(self):
        """Czy faktura jest zaległa?"""
        if self.payment_status in ['paid']:
            return False
        if not self.due_date:
            return False
        from django.utils import timezone
        return self.due_date < timezone.now().date()


class ERPDeliveryNote(models.Model):
    """
    Cache dokumentów WZ z ERP
    """
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='erp_delivery_notes',
        help_text="Firma której dotyczy dokument"
    )
    document_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="ID dokumentu w ERP"
    )
    document_number = models.CharField(max_length=100)
    document_type = models.CharField(max_length=10, default='WZ')
    document_date = models.DateField()

    related_invoice = models.CharField(
        max_length=100,
        blank=True,
        help_text="Powiązana faktura"
    )
    related_order = models.CharField(
        max_length=100,
        blank=True,
        help_text="Powiązane zamówienie"
    )

    # Raw data from ERP (JSON)
    raw_data = models.JSONField(
        null=True,
        blank=True,
        help_text="Pełne dane z API ERP"
    )

    last_synced = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-document_date']
        verbose_name = "Dokument WZ ERP"
        verbose_name_plural = "Dokumenty WZ ERP"

    def __str__(self):
        return f"{self.document_number} - {self.company.name}"
