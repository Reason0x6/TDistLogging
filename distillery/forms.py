from django import forms
from .models import FermentationRecord, DistillationRecord, TotalsRecord, ProductRecord


class FermentationRecordForm(forms.ModelForm):
    """Form for fermentation records"""
    class Meta:
        model = FermentationRecord
        fields = ['description', 'to_field', 'volume_in_l', 'start_date', 'sg_start', 'date', 'sg_end', 'abv', 'lal']
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Fermentation'}),
            'to_field': forms.TextInput(attrs={'placeholder': 'e.g., Fermenter 1'}),
            'volume_in_l': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 100.00'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'sg_start': forms.NumberInput(attrs={'step': '0.0001', 'placeholder': 'e.g., 1.0500'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'sg_end': forms.NumberInput(attrs={'step': '0.0001', 'placeholder': 'e.g., 0.9900'}),
            'abv': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 8.50'}),
            'lal': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 8.50'}),
        }


class DistillationRecordForm(forms.ModelForm):
    """Form for distillation records (Wash, Spirit 1, Spirit 2)"""
    class Meta:
        model = DistillationRecord
        fields = [
            'description', 'faints_in_l', 'from_field', 'to_field', 'volume_in_l',
            'start_date', 'date', 'abv_harts', 'lal',
            'fores_out', 'heads_out', 'harts_out', 'tails_out', 'waste_out'
        ]
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'e.g., Wash Run'}),
            'faints_in_l': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 10.00'}),
            'from_field': forms.TextInput(attrs={'placeholder': 'e.g., Fermenter 1'}),
            'to_field': forms.TextInput(attrs={'placeholder': 'e.g., Still A'}),
            'volume_in_l': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 100.00'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'abv_harts': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 65.00'}),
            'lal': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 45.00'}),
            'fores_out': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 0.50'}),
            'heads_out': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 2.00'}),
            'harts_out': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 70.00'}),
            'tails_out': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 5.00'}),
            'waste_out': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 20.00'}),
        }


class TotalsRecordForm(forms.ModelForm):
    """Form for totals records"""
    class Meta:
        model = TotalsRecord
        fields = ['description', 'faints_to_storage_l', 'faints_abv']
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Totals'}),
            'faints_to_storage_l': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 50.00'}),
            'faints_abv': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 25.00'}),
        }


class ProductRecordForm(forms.ModelForm):
    """Form for product records"""
    class Meta:
        model = ProductRecord
        fields = ['product_name', 'final_abv', 'final_l', 'distillation_location', 'lal']
        widgets = {
            'product_name': forms.TextInput(attrs={'placeholder': 'e.g., A, B, C'}),
            'final_abv': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 40.00'}),
            'final_l': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 100.00'}),
            'distillation_location': forms.TextInput(attrs={'placeholder': 'e.g., Tank 1'}),
            'lal': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 40.00'}),
        }
