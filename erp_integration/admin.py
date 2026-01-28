"""
Admin panel dla modułu integracji ERP
"""

from django.contrib import admin
from .models import (
    ERPSyncLog,
    ERPCustomerCache,
    ERPOrder,
    ERPInvoice,
    ERPDeliveryNote,
)


@admin.register(ERPSyncLog)
class ERPSyncLogAdmin(admin.ModelAdmin):
    """Admin dla logów synchronizacji"""

    list_display = [
        'started_at',
        'sync_type',
        'company',
        'status',
        'records_synced',
        'duration_seconds',
    ]
    list_filter = ['status', 'sync_type', 'started_at']
    search_fields = ['company__name', 'error_message']
    readonly_fields = [
        'started_at',
        'completed_at',
        'duration_seconds',
        'records_synced',
        'error_message',
    ]
    date_hierarchy = 'started_at'

    def has_add_permission(self, request):
        """Logi są tworzone automatycznie"""
        return False


@admin.register(ERPCustomerCache)
class ERPCustomerCacheAdmin(admin.ModelAdmin):
    """Admin dla cache kontrahentów"""

    list_display = [
        'customer_code',
        'name',
        'company',
        'balance',
        'credit_limit',
        'last_synced',
    ]
    list_filter = ['last_synced']
    search_fields = ['customer_code', 'name', 'nip', 'company__name']
    readonly_fields = ['last_synced', 'created_at']
    date_hierarchy = 'last_synced'

    fieldsets = (
        ('Powiązanie', {
            'fields': ('company', 'customer_code')
        }),
        ('Dane kontrahenta', {
            'fields': ('name', 'nip', 'email', 'phone', 'address')
        }),
        ('Finanse', {
            'fields': ('credit_limit', 'balance', 'payment_terms')
        }),
        ('Metadane', {
            'fields': ('last_synced', 'created_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ERPOrder)
class ERPOrderAdmin(admin.ModelAdmin):
    """Admin dla zamówień z ERP"""

    list_display = [
        'order_number',
        'company',
        'order_date',
        'total_gross',
        'currency',
        'status',
        'last_synced',
    ]
    list_filter = ['status', 'order_date', 'currency']
    search_fields = ['order_number', 'order_id', 'company__name']
    readonly_fields = ['order_id', 'last_synced', 'created_at', 'raw_data']
    date_hierarchy = 'order_date'

    fieldsets = (
        ('Podstawowe', {
            'fields': ('company', 'order_id', 'order_number', 'order_date', 'status')
        }),
        ('Finansowe', {
            'fields': ('total_net', 'total_gross', 'currency')
        }),
        ('Realizacja', {
            'fields': ('delivery_date',)
        }),
        ('Metadane', {
            'fields': ('last_synced', 'created_at'),
            'classes': ('collapse',)
        }),
        ('Raw Data (backup)', {
            'fields': ('raw_data',),
            'classes': ('collapse',)
        }),
    )


@admin.register(ERPInvoice)
class ERPInvoiceAdmin(admin.ModelAdmin):
    """Admin dla faktur z ERP"""

    list_display = [
        'invoice_number',
        'invoice_type',
        'company',
        'invoice_date',
        'due_date',
        'total_gross',
        'payment_status',
        'last_synced',
    ]
    list_filter = ['invoice_type', 'payment_status', 'invoice_date', 'currency']
    search_fields = ['invoice_number', 'invoice_id', 'company__name']
    readonly_fields = ['invoice_id', 'last_synced', 'created_at', 'raw_data']
    date_hierarchy = 'invoice_date'

    fieldsets = (
        ('Podstawowe', {
            'fields': ('company', 'invoice_id', 'invoice_number', 'invoice_type')
        }),
        ('Daty', {
            'fields': ('invoice_date', 'sale_date', 'due_date')
        }),
        ('Finansowe', {
            'fields': ('total_net', 'total_gross', 'currency')
        }),
        ('Płatności', {
            'fields': ('payment_status', 'paid_amount', 'remaining_amount')
        }),
        ('Metadane', {
            'fields': ('last_synced', 'created_at'),
            'classes': ('collapse',)
        }),
        ('Raw Data (backup)', {
            'fields': ('raw_data',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Optymalizuj zapytania"""
        qs = super().get_queryset(request)
        return qs.select_related('company')


@admin.register(ERPDeliveryNote)
class ERPDeliveryNoteAdmin(admin.ModelAdmin):
    """Admin dla dokumentów WZ z ERP"""

    list_display = [
        'document_number',
        'document_type',
        'company',
        'document_date',
        'related_invoice',
        'related_order',
        'last_synced',
    ]
    list_filter = ['document_type', 'document_date']
    search_fields = [
        'document_number',
        'document_id',
        'company__name',
        'related_invoice',
        'related_order',
    ]
    readonly_fields = ['document_id', 'last_synced', 'created_at', 'raw_data']
    date_hierarchy = 'document_date'

    fieldsets = (
        ('Podstawowe', {
            'fields': ('company', 'document_id', 'document_number', 'document_type', 'document_date')
        }),
        ('Powiązania', {
            'fields': ('related_invoice', 'related_order')
        }),
        ('Metadane', {
            'fields': ('last_synced', 'created_at'),
            'classes': ('collapse',)
        }),
        ('Raw Data (backup)', {
            'fields': ('raw_data',),
            'classes': ('collapse',)
        }),
    )
