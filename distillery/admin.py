from django.contrib import admin
from .models import Batch, FermentationRecord, DistillationRecord, TotalsRecord, ProductRecord


@admin.register(FermentationRecord)
class FermentationRecordAdmin(admin.ModelAdmin):
    list_display = ('description', 'to_field', 'volume_in_l', 'start_date', 'date', 'abv', 'lal')
    list_filter = ('start_date', 'date')
    search_fields = ('description', 'to_field')
    date_hierarchy = 'date'


@admin.register(DistillationRecord)
class DistillationRecordAdmin(admin.ModelAdmin):
    list_display = ('description', 'from_field', 'to_field', 'volume_in_l', 'start_date', 'date', 'abv_harts', 'lal')
    list_filter = ('start_date', 'date')
    search_fields = ('description', 'from_field', 'to_field')
    date_hierarchy = 'date'


@admin.register(TotalsRecord)
class TotalsRecordAdmin(admin.ModelAdmin):
    list_display = ('description', 'faints_to_storage_l', 'faints_abv', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('description',)
    date_hierarchy = 'created_at'


@admin.register(ProductRecord)
class ProductRecordAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'totals_record', 'final_abv', 'final_l', 'distillation_location', 'lal')
    list_filter = ('product_name', 'created_at')
    search_fields = ('product_name', 'distillation_location')
    date_hierarchy = 'created_at'


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('batch_number', 'recipe', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('batch_number', 'recipe')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

