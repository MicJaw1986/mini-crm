from django import forms
from .models import Interaction
from contacts.models import Contact, Company


class InteractionForm(forms.ModelForm):
    """Formularz dla interakcji"""

    class Meta:
        model = Interaction
        fields = [
            'contact', 'company', 'interaction_type', 'subject',
            'description', 'interaction_date', 'duration_minutes',
            'attachments', 'is_important'
        ]
        widgets = {
            'contact': forms.Select(attrs={'class': 'form-select'}),
            'company': forms.Select(attrs={'class': 'form-select'}),
            'interaction_type': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Np. Spotkanie handlowe'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Szczegóły interakcji...'}),
            'interaction_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '30'}),
            'attachments': forms.FileInput(attrs={'class': 'form-control'}),
            'is_important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        contact_id = kwargs.pop('contact_id', None)
        company_id = kwargs.pop('company_id', None)
        super().__init__(*args, **kwargs)

        # Filtruj kontakty i firmy tylko dla zalogowanego użytkownika
        if self.user:
            self.fields['contact'].queryset = Contact.objects.filter(owner=self.user)
            self.fields['company'].queryset = Company.objects.filter(owner=self.user)

        # Ustaw domyślne wartości jeśli przekazano contact_id lub company_id
        if contact_id:
            self.fields['contact'].initial = contact_id
        if company_id:
            self.fields['company'].initial = company_id

        # Dodaj pustą opcję
        self.fields['contact'].empty_label = '--- Wybierz kontakt (opcjonalnie) ---'
        self.fields['company'].empty_label = '--- Wybierz firmę (opcjonalnie) ---'

    def clean(self):
        cleaned_data = super().clean()
        contact = cleaned_data.get('contact')
        company = cleaned_data.get('company')

        if not contact and not company:
            raise forms.ValidationError('Musisz wybrać kontakt lub firmę.')

        if contact and company:
            if contact.company != company:
                raise forms.ValidationError('Wybrany kontakt nie należy do wybranej firmy.')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user and not instance.pk:
            instance.owner = self.user
        if commit:
            instance.save()
        return instance


class InteractionSearchForm(forms.Form):
    """Formularz wyszukiwania interakcji"""

    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Szukaj po temacie, opisie...'
        })
    )
    interaction_type = forms.ChoiceField(
        required=False,
        choices=[('', 'Wszystkie typy')] + Interaction.TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    contact = forms.ModelChoiceField(
        required=False,
        queryset=Contact.objects.none(),
        empty_label='Wszystkie kontakty',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    company = forms.ModelChoiceField(
        required=False,
        queryset=Company.objects.none(),
        empty_label='Wszystkie firmy',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    is_important = forms.NullBooleanField(
        required=False,
        widget=forms.Select(
            choices=[('', 'Wszystkie'), ('true', 'Tylko ważne'), ('false', 'Nieważne')],
            attrs={'class': 'form-select'}
        )
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['contact'].queryset = Contact.objects.filter(owner=user)
            self.fields['company'].queryset = Company.objects.filter(owner=user)
