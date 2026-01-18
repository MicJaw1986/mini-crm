from django.contrib import admin
from .models import Contact, Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Panel administracyjny dla firm"""
    list_display = ['name', 'industry', 'city', 'owner', 'created_at']
    list_filter = ['industry', 'city', 'created_at']
    search_fields = ['name', 'nip', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Dane podstawowe', {
            'fields': ('name', 'nip', 'industry', 'website')
        }),
        ('Kontakt', {
            'fields': ('phone', 'email')
        }),
        ('Adres', {
            'fields': ('street', 'city', 'postal_code', 'country')
        }),
        ('Dodatkowe informacje', {
            'fields': ('notes', 'owner')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Panel administracyjny dla kontaktów"""
    list_display = ['first_name', 'last_name', 'email', 'company', 'status', 'owner', 'created_at']
    list_filter = ['status', 'company', 'created_at', 'last_contact_date']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'mobile', 'company__name']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['company']
    fieldsets = (
        ('Dane podstawowe', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Kontakt', {
            'fields': ('phone', 'mobile')
        }),
        ('Powiązania', {
            'fields': ('company', 'position')
        }),
        ('Status i kategorie', {
            'fields': ('status', 'tags')
        }),
        ('Adres', {
            'fields': ('street', 'city', 'postal_code', 'country'),
            'classes': ('collapse',)
        }),
        ('Dodatkowe informacje', {
            'fields': ('notes', 'owner', 'last_contact_date')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
