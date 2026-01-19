from django.contrib import admin
from .models import Record, Batch


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('description', 'from_field', 'to_field', 'volume_in_l', 'start_date', 'date', 'abv', 'lal')
    list_filter = ('start_date', 'date')
    search_fields = ('description', 'from_field', 'to_field')
    date_hierarchy = 'date'


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('batch_number', 'recipe', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('batch_number', 'recipe')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

