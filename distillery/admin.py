from django.contrib import admin
from .models import Record


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('description', 'from_field', 'to_field', 'volume_in_l', 'start_date', 'date', 'abv', 'lal')
    list_filter = ('start_date', 'date')
    search_fields = ('description', 'from_field', 'to_field')
    date_hierarchy = 'date'
