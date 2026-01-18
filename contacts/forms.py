from django import forms
from .models import Contact, Company


class CompanyForm(forms.ModelForm):
    """Formularz dla firm"""

    class Meta:
        model = Company
        fields = [
            'name', 'nip', 'industry', 'website', 'phone', 'email',
            'street', 'city', 'postal_code', 'country', 'notes'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nazwa firmy'}),
            'nip': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234567890'}),
            'industry': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'IT, Produkcja, itp.'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+48 123 456 789'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'kontakt@firma.pl'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ul. Przykładowa 123'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Warszawa'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00-000'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Dodatkowe notatki...'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user and not instance.pk:
            instance.owner = self.user
        if commit:
            instance.save()
        return instance


class ContactForm(forms.ModelForm):
    """Formularz dla kontaktów"""

    class Meta:
        model = Contact
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'mobile',
            'company', 'position', 'status', 'tags',
            'street', 'city', 'postal_code', 'country',
            'notes', 'last_contact_date'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jan'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kowalski'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'jan.kowalski@email.pl'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+48 123 456 789'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+48 987 654 321'}),
            'company': forms.Select(attrs={'class': 'form-select'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dyrektor, Manager, itp.'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'vip, partner, supplier'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ul. Przykładowa 123'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Warszawa'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00-000'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Dodatkowe notatki...'}),
            'last_contact_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filtruj firmy tylko dla zalogowanego użytkownika
        if self.user:
            self.fields['company'].queryset = Company.objects.filter(owner=self.user)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user and not instance.pk:
            instance.owner = self.user
        if commit:
            instance.save()
        return instance


class ContactSearchForm(forms.Form):
    """Formularz wyszukiwania kontaktów"""

    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Szukaj po imieniu, nazwisku, email...'
        })
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'Wszystkie statusy')] + Contact.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    company = forms.ModelChoiceField(
        required=False,
        queryset=Company.objects.none(),
        empty_label='Wszystkie firmy',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['company'].queryset = Company.objects.filter(owner=user)


class CompanySearchForm(forms.Form):
    """Formularz wyszukiwania firm"""

    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Szukaj po nazwie, NIP, branży...'
        })
    )
    industry = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Branża'
        })
    )
