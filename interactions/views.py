from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from datetime import datetime
from .models import Interaction
from .forms import InteractionForm, InteractionSearchForm


@login_required
def interaction_list(request):
    """Lista interakcji z wyszukiwaniem i filtrowaniem"""
    interactions = Interaction.objects.filter(owner=request.user).select_related('contact', 'company')

    search_form = InteractionSearchForm(request.GET, user=request.user)

    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        interaction_type = search_form.cleaned_data.get('interaction_type')
        contact = search_form.cleaned_data.get('contact')
        company = search_form.cleaned_data.get('company')
        is_important = search_form.cleaned_data.get('is_important')
        date_from = search_form.cleaned_data.get('date_from')
        date_to = search_form.cleaned_data.get('date_to')

        if query:
            interactions = interactions.filter(
                Q(subject__icontains=query) |
                Q(description__icontains=query)
            )

        if interaction_type:
            interactions = interactions.filter(interaction_type=interaction_type)

        if contact:
            interactions = interactions.filter(contact=contact)

        if company:
            interactions = interactions.filter(company=company)

        if is_important is not None:
            interactions = interactions.filter(is_important=is_important)

        if date_from:
            interactions = interactions.filter(interaction_date__date__gte=date_from)

        if date_to:
            interactions = interactions.filter(interaction_date__date__lte=date_to)

    context = {
        'interactions': interactions,
        'search_form': search_form,
        'total_count': interactions.count(),
    }
    return render(request, 'interactions/interaction_list.html', context)


@login_required
def interaction_detail(request, pk):
    """Szczegóły interakcji"""
    interaction = get_object_or_404(Interaction, pk=pk, owner=request.user)

    context = {
        'interaction': interaction,
    }
    return render(request, 'interactions/interaction_detail.html', context)


@login_required
def interaction_create(request):
    """Tworzenie nowej interakcji"""
    contact_id = request.GET.get('contact')
    company_id = request.GET.get('company')

    if request.method == 'POST':
        form = InteractionForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            interaction = form.save()
            messages.success(request, f'Interakcja "{interaction.subject}" została utworzona.')

            # Przekieruj do odpowiedniego miejsca
            if interaction.contact:
                return redirect('contacts:contact_detail', pk=interaction.contact.pk)
            elif interaction.company:
                return redirect('contacts:company_detail', pk=interaction.company.pk)
            else:
                return redirect('interactions:interaction_list')
    else:
        form = InteractionForm(user=request.user, contact_id=contact_id, company_id=company_id)

    context = {
        'form': form,
        'action': 'Dodaj'
    }
    return render(request, 'interactions/interaction_form.html', context)


@login_required
def interaction_update(request, pk):
    """Edycja interakcji"""
    interaction = get_object_or_404(Interaction, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = InteractionForm(request.POST, request.FILES, instance=interaction, user=request.user)
        if form.is_valid():
            interaction = form.save()
            messages.success(request, f'Interakcja "{interaction.subject}" została zaktualizowana.')
            return redirect('interactions:interaction_detail', pk=interaction.pk)
    else:
        form = InteractionForm(instance=interaction, user=request.user)

    context = {
        'form': form,
        'interaction': interaction,
        'action': 'Edytuj'
    }
    return render(request, 'interactions/interaction_form.html', context)


@login_required
def interaction_delete(request, pk):
    """Usuwanie interakcji"""
    interaction = get_object_or_404(Interaction, pk=pk, owner=request.user)

    if request.method == 'POST':
        subject = interaction.subject
        related_contact = interaction.contact
        related_company = interaction.company
        interaction.delete()
        messages.success(request, f'Interakcja "{subject}" została usunięta.')

        # Przekieruj do odpowiedniego miejsca
        if related_contact:
            return redirect('contacts:contact_detail', pk=related_contact.pk)
        elif related_company:
            return redirect('contacts:company_detail', pk=related_company.pk)
        else:
            return redirect('interactions:interaction_list')

    context = {
        'interaction': interaction,
    }
    return render(request, 'interactions/interaction_confirm_delete.html', context)


@login_required
def interaction_timeline(request):
    """Widok timeline wszystkich interakcji"""
    interactions = Interaction.objects.filter(owner=request.user).select_related('contact', 'company').order_by('-interaction_date')

    context = {
        'interactions': interactions,
        'total_count': interactions.count(),
    }
    return render(request, 'interactions/interaction_timeline.html', context)
