from django.db import models
from django.contrib.auth.models import User
from contacts.models import Contact, Company


class Interaction(models.Model):
    """Model reprezentujący interakcję z klientem"""

    TYPE_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Telefon'),
        ('meeting', 'Spotkanie'),
        ('note', 'Notatka'),
        ('call', 'Połączenie'),
        ('other', 'Inne'),
    ]

    # Powiązania
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        verbose_name='Kontakt',
        related_name='interactions',
        null=True,
        blank=True
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name='Firma',
        related_name='interactions',
        null=True,
        blank=True
    )

    # Dane interakcji
    interaction_type = models.CharField('Typ interakcji', max_length=20, choices=TYPE_CHOICES)
    subject = models.CharField('Temat', max_length=200)
    description = models.TextField('Opis')
    interaction_date = models.DateTimeField('Data interakcji')

    # Dodatkowe pola
    duration_minutes = models.PositiveIntegerField(
        'Czas trwania (minuty)',
        null=True,
        blank=True,
        help_text='Dla spotkań i połączeń'
    )
    attachments = models.FileField(
        'Załączniki',
        upload_to='interactions/%Y/%m/',
        blank=True,
        null=True
    )
    is_important = models.BooleanField('Oznacz jako ważne', default=False)

    # Metadata
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Właściciel', related_name='interactions')
    created_at = models.DateTimeField('Data utworzenia', auto_now_add=True)
    updated_at = models.DateTimeField('Data aktualizacji', auto_now=True)

    class Meta:
        verbose_name = 'Interakcja'
        verbose_name_plural = 'Interakcje'
        ordering = ['-interaction_date']

    def __str__(self):
        target = self.contact or self.company or 'Brak powiązania'
        return f"{self.get_interaction_type_display()} - {target} ({self.interaction_date.strftime('%d.%m.%Y')})"

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.contact and not self.company:
            raise ValidationError('Musisz wybrać kontakt lub firmę.')
        if self.contact and self.company:
            if self.contact.company != self.company:
                raise ValidationError('Kontakt nie należy do wybranej firmy.')

    def get_related_object(self):
        """Zwraca powiązany obiekt (kontakt lub firma)"""
        return self.contact if self.contact else self.company

    def get_related_object_name(self):
        """Zwraca nazwę powiązanego obiektu"""
        if self.contact:
            return self.contact.get_full_name()
        elif self.company:
            return self.company.name
        return 'Brak powiązania'
