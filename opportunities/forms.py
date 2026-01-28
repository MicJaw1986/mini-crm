"""
Formularze dla aplikacji Opportunities

CZYTAJ KOMENTARZE - Dowiesz się jak tworzyć zaawansowane formularze Django!
"""

from django import forms
from .models import Opportunity
from contacts.models import Contact, Company


class OpportunityForm(forms.ModelForm):
    """
    Formularz dla Opportunity (Szansa sprzedaży)

    Co robi ten formularz?
    - Pozwala tworzyć i edytować szanse sprzedażowe
    - Filtruje contact/company - pokazuje tylko należące do użytkownika
    - Waliduje prawdopodobieństwo (0-100%)
    - Stylizuje pola za pomocą Bootstrap 5
    """

    class Meta:
        model = Opportunity
        fields = [
            'name',
            'description',
            'amount',
            'probability',
            'stage',
            'expected_close_date',
            'actual_close_date',
            'contact',
            'company',
            'lost_reason',
            'lost_reason_details'
        ]

        # Widgety - jak pole ma wyglądać w HTML
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'np. Wdrożenie CRM dla Acme Corp'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Szczegóły szansy sprzedażowej...'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'probability': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '50',
                'min': '0',
                'max': '100'
            }),
            'stage': forms.Select(attrs={
                'class': 'form-select'
            }),
            'expected_close_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'  # HTML5 date picker
            }),
            'actual_close_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'contact': forms.Select(attrs={
                'class': 'form-select'
            }),
            'company': forms.Select(attrs={
                'class': 'form-select'
            }),
            'lost_reason': forms.Select(attrs={
                'class': 'form-select'
            }),
            'lost_reason_details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dodatkowe informacje...'
            }),
        }

    def __init__(self, *args, **kwargs):
        """
        Inicjalizacja formularza

        Co się tutaj dzieje?
        1. Wyciągamy użytkownika z kwargs
        2. Inicjalizujemy formularz
        3. Filtrujemy querysety (contact/company) - BEZPIECZEŃSTWO!
        4. Ustawiamy pola jako opcjonalne gdzie trzeba
        """
        # Pobierz użytkownika (przekazanego z widoku)
        self.user = kwargs.pop('user', None)

        # Wywołaj __init__ z klasy nadrzędnej (ModelForm)
        super().__init__(*args, **kwargs)

        # WAŻNE DLA BEZPIECZEŃSTWA!
        # Filtruj contact i company - pokaż tylko należące do użytkownika
        if self.user:
            self.fields['contact'].queryset = Contact.objects.filter(owner=self.user)
            self.fields['company'].queryset = Company.objects.filter(owner=self.user)

        # Ustaw pola jako opcjonalne (nie required)
        self.fields['description'].required = False
        self.fields['contact'].required = False
        self.fields['company'].required = False
        self.fields['actual_close_date'].required = False
        self.fields['lost_reason'].required = False
        self.fields['lost_reason_details'].required = False

        # Dodaj pustą opcję (--- Wybierz ---)
        self.fields['contact'].empty_label = '--- Wybierz kontakt (opcjonalnie) ---'
        self.fields['company'].empty_label = '--- Wybierz firmę (opcjonalnie) ---'
        self.fields['lost_reason'].empty_label = '--- Wybierz powód (jeśli przegrana) ---'

    def clean_probability(self):
        """
        Walidacja prawdopodobieństwa

        Metody clean_NAZWA_POLA() uruchamiają się automatycznie
        podczas walidacji formularza

        Sprawdzamy czy:
        - Prawdopodobieństwo jest w zakresie 0-100
        """
        probability = self.cleaned_data.get('probability')

        if probability is not None:
            if probability < 0 or probability > 100:
                raise forms.ValidationError(
                    'Prawdopodobieństwo musi być w zakresie 0-100%'
                )

        return probability

    def clean(self):
        """
        Walidacja całego formularza

        Sprawdzamy logikę biznesową:
        - Jeśli stage = closed_lost, powinien być lost_reason
        - Jeśli stage = closed_won/lost, powinno być actual_close_date
        """
        cleaned_data = super().clean()
        stage = cleaned_data.get('stage')
        lost_reason = cleaned_data.get('lost_reason')
        actual_close_date = cleaned_data.get('actual_close_date')

        # Jeśli przegrana - wymagaj powodu
        if stage == 'closed_lost' and not lost_reason:
            self.add_error('lost_reason', 'Wybierz powód przegranej')

        # Jeśli zamknięta (won/lost) - wymagaj actual_close_date
        if stage in ['closed_won', 'closed_lost'] and not actual_close_date:
            self.add_error('actual_close_date', 'Podaj rzeczywistą datę zamknięcia')

        return cleaned_data


# PODSUMOWANIE - Co się nauczyłeś:
# 1. ModelForm - automatyczne tworzenie formularza z modelu
# 2. widgets - stylizacja pól (Bootstrap classes)
# 3. __init__() - filtrowanie querysetów dla bezpieczeństwa
# 4. clean_FIELD() - walidacja pojedynczego pola
# 5. clean() - walidacja całego formularza (logika biznesowa)
# 6. HTML5 input types - type="date", min/max, step
# 7. empty_label - pusty wybór w select
