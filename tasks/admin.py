from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Panel administracyjny dla zadań"""
    list_display = ['title', 'status', 'priority', 'get_related_name', 'due_date', 'owner', 'assigned_to']
    list_filter = ['status', 'priority', 'due_date', 'created_at']
    search_fields = ['title', 'description', 'contact__first_name', 'contact__last_name', 'company__name']
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
    date_hierarchy = 'due_date'

    fieldsets = (
        ('Dane podstawowe', {
            'fields': ('title', 'description', 'status', 'priority')
        }),
        ('Terminy', {
            'fields': ('due_date', 'reminder_date')
        }),
        ('Powiązania', {
            'fields': ('contact', 'company', 'owner', 'assigned_to')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )

    def get_related_name(self, obj):
        """Wyświetla nazwę powiązanego kontaktu lub firmy"""
        return obj.get_related_object_name() or '-'
    get_related_name.short_description = 'Powiązane z'

    actions = ['mark_as_done', 'mark_as_in_progress', 'mark_as_todo']

    def mark_as_done(self, request, queryset):
        """Oznacz zadania jako wykonane"""
        updated = queryset.update(status='done')
        self.message_user(request, f'{updated} zadań oznaczono jako wykonane.')
    mark_as_done.short_description = 'Oznacz jako wykonane'

    def mark_as_in_progress(self, request, queryset):
        """Oznacz zadania jako w trakcie"""
        updated = queryset.update(status='in_progress')
        self.message_user(request, f'{updated} zadań oznaczono jako w trakcie.')
    mark_as_in_progress.short_description = 'Oznacz jako w trakcie'

    def mark_as_todo(self, request, queryset):
        """Oznacz zadania jako do zrobienia"""
        updated = queryset.update(status='todo')
        self.message_user(request, f'{updated} zadań oznaczono jako do zrobienia.')
    mark_as_todo.short_description = 'Oznacz jako do zrobienia'
