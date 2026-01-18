from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Task
from .forms import TaskForm, TaskSearchForm


@login_required
def task_list(request):
    """Lista zadań z wyszukiwaniem i filtrowaniem"""
    tasks = Task.objects.filter(owner=request.user).select_related('contact', 'company', 'assigned_to')

    search_form = TaskSearchForm(request.GET, user=request.user)

    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        status = search_form.cleaned_data.get('status')
        priority = search_form.cleaned_data.get('priority')
        contact = search_form.cleaned_data.get('contact')
        company = search_form.cleaned_data.get('company')
        overdue_only = search_form.cleaned_data.get('overdue_only')

        if query:
            tasks = tasks.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        if status:
            tasks = tasks.filter(status=status)

        if priority:
            tasks = tasks.filter(priority=priority)

        if contact:
            tasks = tasks.filter(contact=contact)

        if company:
            tasks = tasks.filter(company=company)

        if overdue_only:
            tasks = [task for task in tasks if task.is_overdue()]

    context = {
        'tasks': tasks,
        'search_form': search_form,
        'total_count': len(tasks) if isinstance(tasks, list) else tasks.count(),
    }
    return render(request, 'tasks/task_list.html', context)


@login_required
def task_detail(request, pk):
    """Szczegóły zadania"""
    task = get_object_or_404(Task, pk=pk, owner=request.user)

    context = {
        'task': task,
    }
    return render(request, 'tasks/task_detail.html', context)


@login_required
def task_create(request):
    """Tworzenie nowego zadania"""
    contact_id = request.GET.get('contact')
    company_id = request.GET.get('company')

    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            task = form.save()
            messages.success(request, f'Zadanie "{task.title}" zostało utworzone.')

            # Przekieruj do odpowiedniego miejsca
            if task.contact:
                return redirect('contacts:contact_detail', pk=task.contact.pk)
            elif task.company:
                return redirect('contacts:company_detail', pk=task.company.pk)
            else:
                return redirect('tasks:task_list')
    else:
        form = TaskForm(user=request.user, contact_id=contact_id, company_id=company_id)

    context = {
        'form': form,
        'action': 'Dodaj'
    }
    return render(request, 'tasks/task_form.html', context)


@login_required
def task_update(request, pk):
    """Edycja zadania"""
    task = get_object_or_404(Task, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            task = form.save()
            messages.success(request, f'Zadanie "{task.title}" zostało zaktualizowane.')
            return redirect('tasks:task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task, user=request.user)

    context = {
        'form': form,
        'task': task,
        'action': 'Edytuj'
    }
    return render(request, 'tasks/task_form.html', context)


@login_required
def task_delete(request, pk):
    """Usuwanie zadania"""
    task = get_object_or_404(Task, pk=pk, owner=request.user)

    if request.method == 'POST':
        title = task.title
        related_contact = task.contact
        related_company = task.company
        task.delete()
        messages.success(request, f'Zadanie "{title}" zostało usunięte.')

        # Przekieruj do odpowiedniego miejsca
        if related_contact:
            return redirect('contacts:contact_detail', pk=related_contact.pk)
        elif related_company:
            return redirect('contacts:company_detail', pk=related_company.pk)
        else:
            return redirect('tasks:task_list')

    context = {
        'task': task,
    }
    return render(request, 'tasks/task_confirm_delete.html', context)


@login_required
def task_toggle_status(request, pk):
    """Szybka zmiana statusu zadania"""
    task = get_object_or_404(Task, pk=pk, owner=request.user)

    # Cykl statusów: todo -> in_progress -> done -> todo
    status_cycle = {
        'todo': 'in_progress',
        'in_progress': 'done',
        'done': 'todo',
        'cancelled': 'todo'
    }

    task.status = status_cycle.get(task.status, 'todo')
    task.save()

    messages.success(request, f'Status zadania zmieniony na: {task.get_status_display()}')

    # Przekieruj z powrotem lub do listy
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('tasks:task_list')


@login_required
def my_tasks(request):
    """Moje zadania - widok skrótowy"""
    now = timezone.now()

    # Zadania pogrupowane według statusu
    todo_tasks = Task.objects.filter(owner=request.user, status='todo').select_related('contact', 'company')
    in_progress_tasks = Task.objects.filter(owner=request.user, status='in_progress').select_related('contact', 'company')
    overdue_tasks = [task for task in todo_tasks.union(in_progress_tasks) if task.is_overdue()]
    due_soon_tasks = [task for task in todo_tasks.union(in_progress_tasks) if task.is_due_soon()]

    context = {
        'todo_tasks': todo_tasks[:10],
        'in_progress_tasks': in_progress_tasks[:10],
        'overdue_tasks': overdue_tasks[:10],
        'due_soon_tasks': due_soon_tasks[:10],
        'todo_count': todo_tasks.count(),
        'in_progress_count': in_progress_tasks.count(),
        'overdue_count': len(overdue_tasks),
        'due_soon_count': len(due_soon_tasks),
    }
    return render(request, 'tasks/my_tasks.html', context)
