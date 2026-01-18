from django import forms
from .models import Task
from contacts.models import Contact, Company


class TaskForm(forms.ModelForm):
    """Formularz dla zadań"""

    class Meta:
        model = Task
        fields = [
            'title', 'description', 'status', 'priority',
            'due_date', 'reminder_date',
            'contact', 'company', 'assigned_to'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Np. Zadzwonić do klienta'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Szczegóły zadania...'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'reminder_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'contact': forms.Select(attrs={'class': 'form-select'}),
            'company': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
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
            # Dodaj wszystkich użytkowników do listy (dla przyszłych funkcji zespołowych)
            from django.contrib.auth.models import User
            self.fields['assigned_to'].queryset = User.objects.filter(id=self.user.id)

        # Ustaw domyślne wartości
        if contact_id:
            self.fields['contact'].initial = contact_id
        if company_id:
            self.fields['company'].initial = company_id

        # Dodaj puste opcje
        self.fields['contact'].empty_label = '--- Brak powiązania ---'
        self.fields['company'].empty_label = '--- Brak powiązania ---'
        self.fields['assigned_to'].empty_label = '--- Przypisz do mnie ---'

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user and not instance.pk:
            instance.owner = self.user
            # Jeśli nie przypisano, przypisz do właściciela
            if not instance.assigned_to:
                instance.assigned_to = self.user
        if commit:
            instance.save()
        return instance


class TaskSearchForm(forms.Form):
    """Formularz wyszukiwania zadań"""

    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Szukaj po tytule, opisie...'
        })
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'Wszystkie statusy')] + Task.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    priority = forms.ChoiceField(
        required=False,
        choices=[('', 'Wszystkie priorytety')] + Task.PRIORITY_CHOICES,
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
    overdue_only = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['contact'].queryset = Contact.objects.filter(owner=user)
            self.fields['company'].queryset = Company.objects.filter(owner=user)


class QuickTaskForm(forms.ModelForm):
    """Uproszczony formularz szybkiego dodawania zadań"""

    class Meta:
        model = Task
        fields = ['title', 'due_date', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tytuł zadania'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.owner = self.user
            instance.assigned_to = self.user
        if commit:
            instance.save()
        return instance
