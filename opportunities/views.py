"""
Widoki dla aplikacji Opportunities

CZYTAJ KOMENTARZE - Pełny CRUD z logowaniem i filtrowaniem!
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Opportunity
from .forms import OpportunityForm


@login_required
def opportunity_list(view):
    """
    Lista szans sprzedażowych (Opportunities)

    Funkcjonalności:
    - Pokazuje tylko opportunities użytkownika (data isolation)
    - Wyszukiwanie po nazwie, opisie
    - Filtrowanie po stage
    - Sortowanie
    """
    # Pobierz tylko opportunities należące do zalogowanego użytkownika
    opportunities = Opportunity.objects.filter(owner=view.user)

    # WYSZUKIWANIE
    search_query = view.GET.get('search', '')
    if search_query:
        opportunities = opportunities.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(contact__first_name__icontains=search_query) |
            Q(contact__last_name__icontains=search_query) |
            Q(company__name__icontains=search_query)
        )

    # FILTROWANIE po stage
    stage_filter = view.GET.get('stage', '')
    if stage_filter:
        opportunities = opportunities.filter(stage=stage_filter)

    # SORTOWANIE
    # Domyślnie: najbliższe daty zamknięcia na górze
    opportunities = opportunities.order_by('expected_close_date')

    # Statystyki dla dashboardu
    stats = {
        'total': opportunities.count(),
        'open': opportunities.filter(stage__in=['qualification', 'proposal', 'negotiation']).count(),
        'won': opportunities.filter(stage='closed_won').count(),
        'lost': opportunities.filter(stage='closed_lost').count(),
    }

    # Oblicz łączną wartość ważoną (pipeline value)
    pipeline_value = sum(
        opp.get_weighted_value()
        for opp in opportunities.filter(stage__in=['qualification', 'proposal', 'negotiation'])
    )

    context = {
        'opportunities': opportunities,
        'search_query': search_query,
        'stage_filter': stage_filter,
        'stage_choices': Opportunity.STAGE_CHOICES,
        'stats': stats,
        'pipeline_value': pipeline_value,
    }

    return render(view, 'opportunities/opportunity_list.html', context)


@login_required
def opportunity_detail(view, pk):
    """
    Szczegóły pojedynczej szansy sprzedażowej

    Co pokazujemy?
    - Wszystkie informacje o opportunity
    - Powiązany kontakt/firma
    - Wartość ważona
    - Dni do zamknięcia
    - Status (overdue?)
    """
    # get_object_or_404 - pobierz lub 404
    # WAŻNE: Sprawdzamy owner - użytkownik może zobaczyć tylko swoje!
    opportunity = get_object_or_404(
        Opportunity,
        pk=pk,
        owner=view.user
    )

    context = {
        'opportunity': opportunity,
        'weighted_value': opportunity.get_weighted_value(),
        'days_until_close': opportunity.days_until_close(),
        'is_overdue': opportunity.is_overdue(),
    }

    return render(view, 'opportunities/opportunity_detail.html', context)


@login_required
def opportunity_create(view):
    """
    Tworzenie nowej szansy sprzedażowej

    Proces:
    1. GET - pokaż pusty formularz
    2. POST - waliduj i zapisz
    3. Ustaw owner na zalogowanego użytkownika
    4. Przekieruj do listy
    """
    if view.method == 'POST':
        # POST - przetwarzanie formularza
        form = OpportunityForm(view.POST, user=view.user)

        if form.is_valid():
            # Zapisz, ale nie commituj jeszcze (musimy ustawić owner)
            opportunity = form.save(commit=False)
            opportunity.owner = view.user  # BEZPIECZEŃSTWO!
            opportunity.save()

            # Komunikat sukcesu
            messages.success(view, f'Szansa "{opportunity.name}" została utworzona!')

            return redirect('opportunities:opportunity_detail', pk=opportunity.pk)
    else:
        # GET - pokaż pusty formularz
        form = OpportunityForm(user=view.user)

    context = {
        'form': form,
        'action': 'create'
    }

    return render(view, 'opportunities/opportunity_form.html', context)


@login_required
def opportunity_update(view, pk):
    """
    Edycja istniejącej szansy sprzedażowej

    Podobnie jak create, ale:
    - Pobieramy istniejący obiekt
    - Przekazujemy instance do formularza
    """
    # Pobierz opportunity - tylko jeśli należy do użytkownika
    opportunity = get_object_or_404(
        Opportunity,
        pk=pk,
        owner=view.user
    )

    if view.method == 'POST':
        # POST - przetwarzanie formularza
        form = OpportunityForm(view.POST, instance=opportunity, user=view.user)

        if form.is_valid():
            form.save()

            messages.success(view, f'Szansa "{opportunity.name}" została zaktualizowana!')

            return redirect('opportunities:opportunity_detail', pk=opportunity.pk)
    else:
        # GET - pokaż formularz z danymi
        form = OpportunityForm(instance=opportunity, user=view.user)

    context = {
        'form': form,
        'opportunity': opportunity,
        'action': 'update'
    }

    return render(view, 'opportunities/opportunity_form.html', context)


@login_required
def opportunity_delete(view, pk):
    """
    Usuwanie szansy sprzedażowej

    Proces:
    1. GET - pokaż formularz potwierdzenia
    2. POST - usuń i przekieruj
    """
    # Pobierz opportunity - tylko jeśli należy do użytkownika
    opportunity = get_object_or_404(
        Opportunity,
        pk=pk,
        owner=view.user
    )

    if view.method == 'POST':
        # POST - potwierdzone usunięcie
        opportunity_name = opportunity.name
        opportunity.delete()

        messages.success(view, f'Szansa "{opportunity_name}" została usunięta!')

        return redirect('opportunities:opportunity_list')

    # GET - pokaż formularz potwierdzenia
    context = {
        'opportunity': opportunity
    }

    return render(view, 'opportunities/opportunity_confirm_delete.html', context)


@login_required
def opportunity_move_stage(view, pk, new_stage):
    """
    Szybkie przesunięcie opportunity do nowego stage

    URL: /opportunities/<pk>/move/<new_stage>/

    Przykład:
    - /opportunities/5/move/proposal/ - przesuń do propozycji
    - /opportunities/5/move/closed_won/ - oznacz jako wygraną
    """
    opportunity = get_object_or_404(
        Opportunity,
        pk=pk,
        owner=view.user
    )

    # Sprawdź czy stage jest poprawny
    valid_stages = [choice[0] for choice in Opportunity.STAGE_CHOICES]
    if new_stage not in valid_stages:
        messages.error(view, f'Nieprawidłowy etap: {new_stage}')
        return redirect('opportunities:opportunity_detail', pk=pk)

    # Przesuń do nowego stage
    opportunity.move_to_stage(new_stage, user=view.user)

    messages.success(
        view,
        f'Szansa "{opportunity.name}" została przesunięta do: {opportunity.get_stage_display()}'
    )

    return redirect('opportunities:opportunity_detail', pk=pk)


# PODSUMOWANIE - Co się nauczyłeś:
# 1. @login_required - wymuszenie logowania
# 2. get_object_or_404() - bezpieczne pobieranie obiektów
# 3. Data isolation - owner=view.user (BEZPIECZEŃSTWO!)
# 4. Wyszukiwanie - Q objects dla OR queries
# 5. Filtrowanie - filter(stage=...)
# 6. Statystyki - count(), sum()
# 7. Messages framework - messages.success/error
# 8. Form handling - GET vs POST
# 9. commit=False - zapisz bez commitu (żeby ustawić owner)
# 10. instance= - edycja istniejącego obiektu
