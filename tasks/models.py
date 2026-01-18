from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from contacts.models import Contact, Company


class Task(models.Model):
    """Model reprezentujący zadanie"""

    STATUS_CHOICES = [
        ('todo', 'Do zrobienia'),
        ('in_progress', 'W trakcie'),
        ('done', 'Wykonane'),
        ('cancelled', 'Anulowane'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Niska'),
        ('medium', 'Średnia'),
        ('high', 'Wysoka'),
        ('urgent', 'Pilne'),
    ]

    # Podstawowe dane
    title = models.CharField('Tytuł', max_length=200)
    description = models.TextField('Opis', blank=True)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField('Priorytet', max_length=20, choices=PRIORITY_CHOICES, default='medium')

    # Terminy
    due_date = models.DateTimeField('Termin wykonania', null=True, blank=True)
    reminder_date = models.DateTimeField('Data przypomnienia', null=True, blank=True)

    # Powiązania
    contact = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Kontakt',
        related_name='tasks'
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Firma',
        related_name='tasks'
    )

    # Metadata
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Właściciel', related_name='tasks')
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Przypisane do',
        related_name='assigned_tasks'
    )
    created_at = models.DateTimeField('Data utworzenia', auto_now_add=True)
    updated_at = models.DateTimeField('Data aktualizacji', auto_now=True)
    completed_at = models.DateTimeField('Data wykonania', null=True, blank=True)

    class Meta:
        verbose_name = 'Zadanie'
        verbose_name_plural = 'Zadania'
        ordering = ['-priority', 'due_date', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        # Automatycznie ustaw datę wykonania gdy status zmieni się na 'done'
        if self.status == 'done' and not self.completed_at:
            self.completed_at = timezone.now()
        elif self.status != 'done':
            self.completed_at = None
        super().save(*args, **kwargs)

    def is_overdue(self):
        """Sprawdza czy zadanie jest po terminie"""
        if self.due_date and self.status not in ['done', 'cancelled']:
            return timezone.now() > self.due_date
        return False

    def is_due_soon(self):
        """Sprawdza czy zadanie jest do wykonania wkrótce (w ciągu 24h)"""
        if self.due_date and self.status not in ['done', 'cancelled']:
            time_diff = self.due_date - timezone.now()
            return timezone.timedelta(0) < time_diff <= timezone.timedelta(hours=24)
        return False

    def get_related_object(self):
        """Zwraca powiązany obiekt (kontakt lub firma)"""
        return self.contact if self.contact else self.company

    def get_related_object_name(self):
        """Zwraca nazwę powiązanego obiektu"""
        if self.contact:
            return self.contact.get_full_name()
        elif self.company:
            return self.company.name
        return None

    def get_priority_badge_class(self):
        """Zwraca klasę CSS dla badge priorytetu"""
        priority_classes = {
            'low': 'bg-secondary',
            'medium': 'bg-info',
            'high': 'bg-warning text-dark',
            'urgent': 'bg-danger',
        }
        return priority_classes.get(self.priority, 'bg-secondary')
