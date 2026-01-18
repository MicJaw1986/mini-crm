from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import Contact, Company
from .forms import ContactForm, CompanyForm, ContactSearchForm, CompanySearchForm


# Contact Views

@login_required
def contact_list(request):
    """Lista kontaktów z wyszukiwaniem i filtrowaniem"""
    contacts = Contact.objects.filter(owner=request.user).select_related('company')

    search_form = ContactSearchForm(request.GET, user=request.user)

    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        status = search_form.cleaned_data.get('status')
        company = search_form.cleaned_data.get('company')

        if query:
            contacts = contacts.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query) |
                Q(phone__icontains=query) |
                Q(mobile__icontains=query)
            )

        if status:
            contacts = contacts.filter(status=status)

        if company:
            contacts = contacts.filter(company=company)

    context = {
        'contacts': contacts,
        'search_form': search_form,
        'total_count': contacts.count(),
    }
    return render(request, 'contacts/contact_list.html', context)


@login_required
def contact_detail(request, pk):
    """Szczegóły kontaktu"""
    contact = get_object_or_404(Contact, pk=pk, owner=request.user)

    context = {
        'contact': contact,
    }
    return render(request, 'contacts/contact_detail.html', context)


@login_required
def contact_create(request):
    """Tworzenie nowego kontaktu"""
    if request.method == 'POST':
        form = ContactForm(request.POST, user=request.user)
        if form.is_valid():
            contact = form.save()
            messages.success(request, f'Kontakt {contact.get_full_name()} został utworzony.')
            return redirect('contacts:contact_detail', pk=contact.pk)
    else:
        form = ContactForm(user=request.user)

    context = {
        'form': form,
        'action': 'Dodaj'
    }
    return render(request, 'contacts/contact_form.html', context)


@login_required
def contact_update(request, pk):
    """Edycja kontaktu"""
    contact = get_object_or_404(Contact, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact, user=request.user)
        if form.is_valid():
            contact = form.save()
            messages.success(request, f'Kontakt {contact.get_full_name()} został zaktualizowany.')
            return redirect('contacts:contact_detail', pk=contact.pk)
    else:
        form = ContactForm(instance=contact, user=request.user)

    context = {
        'form': form,
        'contact': contact,
        'action': 'Edytuj'
    }
    return render(request, 'contacts/contact_form.html', context)


@login_required
def contact_delete(request, pk):
    """Usuwanie kontaktu"""
    contact = get_object_or_404(Contact, pk=pk, owner=request.user)

    if request.method == 'POST':
        contact_name = contact.get_full_name()
        contact.delete()
        messages.success(request, f'Kontakt {contact_name} został usunięty.')
        return redirect('contacts:contact_list')

    context = {
        'contact': contact,
    }
    return render(request, 'contacts/contact_confirm_delete.html', context)


# Company Views

@login_required
def company_list(request):
    """Lista firm z wyszukiwaniem i filtrowaniem"""
    companies = Company.objects.filter(owner=request.user).annotate(
        contacts_count=Count('contacts')
    )

    search_form = CompanySearchForm(request.GET)

    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        industry = search_form.cleaned_data.get('industry')

        if query:
            companies = companies.filter(
                Q(name__icontains=query) |
                Q(nip__icontains=query) |
                Q(email__icontains=query)
            )

        if industry:
            companies = companies.filter(industry__icontains=industry)

    context = {
        'companies': companies,
        'search_form': search_form,
        'total_count': companies.count(),
    }
    return render(request, 'contacts/company_list.html', context)


@login_required
def company_detail(request, pk):
    """Szczegóły firmy"""
    company = get_object_or_404(Company, pk=pk, owner=request.user)
    contacts = company.contacts.all()

    context = {
        'company': company,
        'contacts': contacts,
    }
    return render(request, 'contacts/company_detail.html', context)


@login_required
def company_create(request):
    """Tworzenie nowej firmy"""
    if request.method == 'POST':
        form = CompanyForm(request.POST, user=request.user)
        if form.is_valid():
            company = form.save()
            messages.success(request, f'Firma {company.name} została utworzona.')
            return redirect('contacts:company_detail', pk=company.pk)
    else:
        form = CompanyForm(user=request.user)

    context = {
        'form': form,
        'action': 'Dodaj'
    }
    return render(request, 'contacts/company_form.html', context)


@login_required
def company_update(request, pk):
    """Edycja firmy"""
    company = get_object_or_404(Company, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company, user=request.user)
        if form.is_valid():
            company = form.save()
            messages.success(request, f'Firma {company.name} została zaktualizowana.')
            return redirect('contacts:company_detail', pk=company.pk)
    else:
        form = CompanyForm(instance=company, user=request.user)

    context = {
        'form': form,
        'company': company,
        'action': 'Edytuj'
    }
    return render(request, 'contacts/company_form.html', context)


@login_required
def company_delete(request, pk):
    """Usuwanie firmy"""
    company = get_object_or_404(Company, pk=pk, owner=request.user)

    if request.method == 'POST':
        company_name = company.name
        company.delete()
        messages.success(request, f'Firma {company_name} została usunięta.')
        return redirect('contacts:company_list')

    context = {
        'company': company,
    }
    return render(request, 'contacts/company_confirm_delete.html', context)
