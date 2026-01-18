from django.contrib import admin
from .models import Interaction


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    """Panel administracyjny dla interakcji"""
    list_display = ['subject', 'interaction_type', 'get_related_name', 'interaction_date', 'is_important', 'owner']
    list_filter = ['interaction_type', 'is_important', 'interaction_date', 'created_at']
    search_fields = ['subject', 'description', 'contact__first_name', 'contact__last_name', 'company__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'interaction_date'

    fieldsets = (
        ('Powiązania', {
            'fields': ('contact', 'company')
        }),
        ('Dane interakcji', {
            'fields': ('interaction_type', 'subject', 'description', 'interaction_date')
        }),
        ('Dodatkowe informacje', {
            'fields': ('duration_minutes', 'attachments', 'is_important', 'owner')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_related_name(self, obj):
        """Wyświetla nazwę powiązanego kontaktu lub firmy"""
        return obj.get_related_object_name()
    get_related_name.short_description = 'Powiązane z'
