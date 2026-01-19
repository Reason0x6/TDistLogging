from django import forms
from .models import Record


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = [
            'description', 'from_field', 'to_field', 'volume_in_l',
            'start_date', 'sg_start', 'date', 'sg_end', 'abv', 'lal'
        ]
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Enter description'}),
            'from_field': forms.TextInput(attrs={'placeholder': 'e.g., Fermenter 1'}),
            'to_field': forms.TextInput(attrs={'placeholder': 'e.g., Still A'}),
            'volume_in_l': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 100.00'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'sg_start': forms.NumberInput(attrs={'step': '0.0001', 'placeholder': 'e.g., 1.0500'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'sg_end': forms.NumberInput(attrs={'step': '0.0001', 'placeholder': 'e.g., 0.9900'}),
            'abv': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 45.00'}),
            'lal': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 45.00'}),
        }
        labels = {
            'from_field': 'From',
            'to_field': 'To',
            'volume_in_l': 'Volume in L',
            'sg_start': 'SG Start',
            'date': 'End Date',
            'sg_end': 'SG End',
            'abv': 'ABV (%)',
            'lal': 'LAL',
        }
