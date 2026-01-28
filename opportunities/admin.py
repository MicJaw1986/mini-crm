from django.contrib import admin
from .models import Opportunity


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    """
    Admin panel dla Opportunity

    Pokazuje wszystkie kluczowe informacje o szansach sprzedaży
    """

    list_display = [
        'name',
        'stage',
        'amount',
        'probability',
        'expected_close_date',
        'contact',
        'company',
        'owner',
        'created_at'
    ]

    list_filter = [
        'stage',
        'owner',
        'created_at',
        'expected_close_date'
    ]

    search_fields = [
        'name',
        'description',
        'contact__first_name',
        'contact__last_name',
        'company__name'
    ]

    readonly_fields = ['created_at', 'updated_at', 'actual_close_date']

    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('name', 'description', 'owner')
        }),
        ('Wartość i etap', {
            'fields': ('amount', 'probability', 'stage')
        }),
        ('Daty', {
            'fields': ('expected_close_date', 'actual_close_date')
        }),
        ('Relacje', {
            'fields': ('contact', 'company')
        }),
        ('Przegrana (jeśli dotyczy)', {
            'fields': ('lost_reason', 'lost_reason_details'),
            'classes': ('collapse',)  # Schowane domyślnie
        }),
        ('Metadane', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
