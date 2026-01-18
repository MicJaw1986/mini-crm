from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from contacts.models import Contact, Company
from interactions.models import Interaction
from tasks.models import Task


@login_required
def dashboard_view(request):
    """Ulepszone dashboard ze statystykami"""
    user = request.user
    now = timezone.now()

    # Statystyki kontaktów
    total_contacts = Contact.objects.filter(owner=user).count()
    contacts_by_status = Contact.objects.filter(owner=user).values('status').annotate(count=Count('id'))

    # Statystyki firm
    total_companies = Company.objects.filter(owner=user).count()
    companies_with_contacts = Company.objects.filter(owner=user).annotate(
        contact_count=Count('contacts')
    ).filter(contact_count__gt=0).count()

    # Statystyki interakcji
    total_interactions = Interaction.objects.filter(owner=user).count()
    interactions_this_month = Interaction.objects.filter(
        owner=user,
        interaction_date__gte=now - timedelta(days=30)
    ).count()
    interactions_by_type = Interaction.objects.filter(owner=user).values('interaction_type').annotate(count=Count('id'))
    recent_interactions = Interaction.objects.filter(owner=user).select_related('contact', 'company').order_by('-interaction_date')[:5]

    # Statystyki zadań
    total_tasks = Task.objects.filter(owner=user).count()
    tasks_by_status = Task.objects.filter(owner=user).values('status').annotate(count=Count('id'))

    # Zadania krytyczne
    overdue_tasks = [task for task in Task.objects.filter(owner=user).exclude(status__in=['done', 'cancelled']) if task.is_overdue()]
    urgent_tasks = Task.objects.filter(
        owner=user,
        priority='urgent',
        status__in=['todo', 'in_progress']
    ).select_related('contact', 'company').order_by('due_date')[:5]
    due_soon_tasks = [task for task in Task.objects.filter(owner=user).exclude(status__in=['done', 'cancelled']) if task.is_due_soon()]

    # Ostatnie aktywności (interakcje i zadania razem)
    recent_tasks = Task.objects.filter(owner=user).select_related('contact', 'company').order_by('-created_at')[:3]

    # Dane do wykresów
    # Statusy kontaktów
    contact_status_data = {item['status']: item['count'] for item in contacts_by_status}
    contact_status_labels = []
    contact_status_values = []
    for status_code, status_name in Contact.STATUS_CHOICES:
        if status_code in contact_status_data:
            contact_status_labels.append(status_name)
            contact_status_values.append(contact_status_data[status_code])

    # Typy interakcji
    interaction_type_data = {item['interaction_type']: item['count'] for item in interactions_by_type}
    interaction_type_labels = []
    interaction_type_values = []
    for type_code, type_name in Interaction.TYPE_CHOICES:
        if type_code in interaction_type_data:
            interaction_type_labels.append(type_name)
            interaction_type_values.append(interaction_type_data[type_code])

    # Statusy zadań
    task_status_data = {item['status']: item['count'] for item in tasks_by_status}
    task_status_labels = []
    task_status_values = []
    task_status_colors = []
    status_color_map = {
        'todo': '#0d6efd',      # blue
        'in_progress': '#ffc107',  # yellow
        'done': '#198754',      # green
        'cancelled': '#6c757d'  # gray
    }
    for status_code, status_name in Task.STATUS_CHOICES:
        if status_code in task_status_data:
            task_status_labels.append(status_name)
            task_status_values.append(task_status_data[status_code])
            task_status_colors.append(status_color_map.get(status_code, '#6c757d'))

    context = {
        # Podstawowe statystyki
        'total_contacts': total_contacts,
        'total_companies': total_companies,
        'total_interactions': total_interactions,
        'total_tasks': total_tasks,
        'companies_with_contacts': companies_with_contacts,
        'interactions_this_month': interactions_this_month,

        # Dane do wykresów
        'contact_status_labels': contact_status_labels,
        'contact_status_values': contact_status_values,
        'interaction_type_labels': interaction_type_labels,
        'interaction_type_values': interaction_type_values,
        'task_status_labels': task_status_labels,
        'task_status_values': task_status_values,
        'task_status_colors': task_status_colors,

        # Listy dla widżetów
        'recent_interactions': recent_interactions,
        'recent_tasks': recent_tasks,
        'overdue_tasks': overdue_tasks[:5],
        'urgent_tasks': urgent_tasks,
        'due_soon_tasks': due_soon_tasks[:5],

        # Liczniki dla widżetów
        'overdue_count': len(overdue_tasks),
        'urgent_count': urgent_tasks.count(),
        'due_soon_count': len(due_soon_tasks),
    }

    return render(request, 'dashboard.html', context)
