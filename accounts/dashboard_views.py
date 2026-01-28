from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from contacts.models import Contact, Company
from interactions.models import Interaction
from tasks.models import Task
from opportunities.models import Opportunity


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

    # Statystyki opportunities (szans sprzedażowych)
    total_opportunities = Opportunity.objects.filter(owner=user).count()
    open_opportunities = Opportunity.objects.filter(
        owner=user,
        stage__in=['qualification', 'proposal', 'negotiation']
    ).count()
    won_opportunities = Opportunity.objects.filter(owner=user, stage='closed_won').count()
    lost_opportunities = Opportunity.objects.filter(owner=user, stage='closed_lost').count()

    # Pipeline value (wartość ważona wszystkich otwartych opportunities)
    pipeline_value = sum(
        opp.get_weighted_value()
        for opp in Opportunity.objects.filter(
            owner=user,
            stage__in=['qualification', 'proposal', 'negotiation']
        )
    )

    # Wartość wygranych opportunities (przychód)
    revenue = sum(
        opp.amount
        for opp in Opportunity.objects.filter(owner=user, stage='closed_won')
    )

    # Opportunities przekroczone (overdue)
    overdue_opportunities = [
        opp for opp in Opportunity.objects.filter(
            owner=user,
            stage__in=['qualification', 'proposal', 'negotiation']
        ) if opp.is_overdue()
    ]

    # Najbliższe zamknięcia (następne 7 dni)
    upcoming_opportunities = Opportunity.objects.filter(
        owner=user,
        stage__in=['qualification', 'proposal', 'negotiation'],
        expected_close_date__gte=now.date(),
        expected_close_date__lte=now.date() + timedelta(days=7)
    ).select_related('contact', 'company').order_by('expected_close_date')[:5]

    # Statystyki według stage
    opportunities_by_stage = Opportunity.objects.filter(owner=user).values('stage').annotate(count=Count('id'))
    opportunity_stage_data = {item['stage']: item['count'] for item in opportunities_by_stage}
    opportunity_stage_labels = []
    opportunity_stage_values = []
    opportunity_stage_colors = []
    stage_color_map = {
        'qualification': '#6c757d',    # gray
        'proposal': '#0dcaf0',         # cyan
        'negotiation': '#ffc107',      # yellow
        'closed_won': '#198754',       # green
        'closed_lost': '#dc3545'       # red
    }
    for stage_code, stage_name in Opportunity.STAGE_CHOICES:
        if stage_code in opportunity_stage_data:
            opportunity_stage_labels.append(stage_name)
            opportunity_stage_values.append(opportunity_stage_data[stage_code])
            opportunity_stage_colors.append(stage_color_map.get(stage_code, '#6c757d'))

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
        'total_opportunities': total_opportunities,
        'companies_with_contacts': companies_with_contacts,
        'interactions_this_month': interactions_this_month,

        # Statystyki opportunities
        'open_opportunities': open_opportunities,
        'won_opportunities': won_opportunities,
        'lost_opportunities': lost_opportunities,
        'pipeline_value': pipeline_value,
        'revenue': revenue,

        # Dane do wykresów
        'contact_status_labels': contact_status_labels,
        'contact_status_values': contact_status_values,
        'interaction_type_labels': interaction_type_labels,
        'interaction_type_values': interaction_type_values,
        'task_status_labels': task_status_labels,
        'task_status_values': task_status_values,
        'task_status_colors': task_status_colors,
        'opportunity_stage_labels': opportunity_stage_labels,
        'opportunity_stage_values': opportunity_stage_values,
        'opportunity_stage_colors': opportunity_stage_colors,

        # Listy dla widżetów
        'recent_interactions': recent_interactions,
        'recent_tasks': recent_tasks,
        'overdue_tasks': overdue_tasks[:5],
        'urgent_tasks': urgent_tasks,
        'due_soon_tasks': due_soon_tasks[:5],
        'overdue_opportunities': overdue_opportunities[:5],
        'upcoming_opportunities': upcoming_opportunities,

        # Liczniki dla widżetów
        'overdue_count': len(overdue_tasks),
        'urgent_count': urgent_tasks.count(),
        'due_soon_count': len(due_soon_tasks),
        'overdue_opportunities_count': len(overdue_opportunities),
    }

    return render(request, 'dashboard.html', context)
