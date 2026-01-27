from django import forms
from .models import FermentationRecord, WashRecord, DistillationRecord, TotalsRecord, ProductRecord


class FermentationRecordForm(forms.ModelForm):
    """Form for fermentation records"""
    class Meta:
        model = FermentationRecord
        fields = ['description', 'to_field', 'volume_in_l', 'start_date', 'sg_start', 'date', 'sg_end', 'abv', 'lal']
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Fermentation'}),
            'to_field': forms.TextInput(attrs={'placeholder': 'e.g., Fermenter 1'}),
            'volume_in_l': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 100.00', 'class': 'calc-input'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'sg_start': forms.NumberInput(attrs={'step': '0.0001', 'placeholder': 'e.g., 1.0500', 'class': 'calc-input'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'sg_end': forms.NumberInput(attrs={'step': '0.0001', 'placeholder': 'e.g., 0.9900', 'class': 'calc-input'}),
            'abv': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Auto-calculated', 'class': 'calc-input', 'readonly': False}),
            'lal': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Auto-calculated', 'class': 'calc-input', 'readonly': False}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        sg_start = cleaned_data.get('sg_start')
        sg_end = cleaned_data.get('sg_end')
        volume_in_l = cleaned_data.get('volume_in_l')
        abv = cleaned_data.get('abv')
        
        # Calculate ABV if SG values are provided and ABV is not manually set
        if sg_start and sg_end and not abv:
            cleaned_data['abv'] = round((sg_start - sg_end) * 131.25, 2)
        
        # Use the calculated or provided ABV for LAL calculation
        abv = cleaned_data.get('abv')
        lal = cleaned_data.get('lal')
        
        # Calculate LAL if volume and ABV are provided and LAL is not manually set
        if volume_in_l and abv and not lal:
            cleaned_data['lal'] = round(float(volume_in_l) * (abv / 100), 2)
        
        return cleaned_data


class WashRecordForm(forms.ModelForm):
    """Form for wash distillation records"""
    class Meta:
        model = WashRecord
        fields = [
            'description', 'faints_in_l', 'from_field', 'to_field', 'volume_in_l',
            'start_date', 'sg_start', 'date', 'sg_end',
            'fores_out', 'heads_out', 'hearts_out', 'hearts_out_location', 'tails_out', 'waste_out',
            'abv_hearts', 'lal'
        ]
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'e.g., Wash Run'}),
            'faints_in_l': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 10.00'}),
            'from_field': forms.TextInput(attrs={'placeholder': 'e.g., Fermenter 1'}),
            'to_field': forms.TextInput(attrs={'placeholder': 'e.g., Still A'}),
            'volume_in_l': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 100.00', 'class': 'calc-input'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'sg_start': forms.NumberInput(attrs={'step': '0.0001', 'placeholder': 'e.g., 1.0500', 'class': 'calc-input'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'sg_end': forms.NumberInput(attrs={'step': '0.0001', 'placeholder': 'e.g., 0.9900', 'class': 'calc-input'}),
            'fores_out': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 0.50'}),
            'heads_out': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 2.00'}),
            'hearts_out': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 70.00'}),
            'hearts_out_location': forms.TextInput(attrs={'placeholder': 'e.g., Tank 1'}),
            'tails_out': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 5.00'}),
            'waste_out': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 20.00'}),
            'abv_hearts': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Auto-calculated', 'class': 'calc-input', 'readonly': False}),
            'lal': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Auto-calculated', 'class': 'calc-input', 'readonly': False}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        sg_start = cleaned_data.get('sg_start')
        sg_end = cleaned_data.get('sg_end')
        volume_in_l = cleaned_data.get('volume_in_l')
        abv_hearts = cleaned_data.get('abv_hearts')
        
        # Calculate ABV if SG values are provided and ABV is not manually set
        if sg_start and sg_end and not abv_hearts:
            cleaned_data['abv_hearts'] = round((sg_start - sg_end) * 131.25, 2)
        
        # Use the calculated or provided ABV for LAL calculation
        abv_hearts = cleaned_data.get('abv_hearts')
        lal = cleaned_data.get('lal')
        
        # Calculate LAL if volume and ABV are provided and LAL is not manually set
        if volume_in_l and abv_hearts and not lal:
            cleaned_data['lal'] = round(float(volume_in_l) * (abv_hearts / 100), 2)
        
        return cleaned_data


class DistillationRecordForm(forms.ModelForm):
    """Form for distillation records (Spirit 1, Spirit 2)"""
    class Meta:
        model = DistillationRecord
        fields = [
            'description', 'faints_in_l', 'from_field', 'to_field', 'volume_in_l',
            'start_date', 'date',
            'fores_out', 'heads_out', 'hearts_out', 'abv_hearts', 'hearts_out_location',
            'tails_out', 'faints_out_location', 'waste_out', 'lal'
        ]
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'e.g., Spirit Run'}),
            'faints_in_l': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 10.00'}),
            'from_field': forms.TextInput(attrs={'placeholder': 'e.g., Tank 1'}),
            'to_field': forms.TextInput(attrs={'placeholder': 'e.g., Still A'}),
            'volume_in_l': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 100.00', 'class': 'calc-input'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'fores_out': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 0.50'}),
            'heads_out': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 2.00'}),
            'hearts_out': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 70.00'}),
            'abv_hearts': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 85.00', 'class': 'calc-input'}),
            'hearts_out_location': forms.TextInput(attrs={'placeholder': 'e.g., Tank 1'}),
            'tails_out': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 5.00'}),
            'faints_out_location': forms.TextInput(attrs={'placeholder': 'e.g., Faints Tank'}),
            'waste_out': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 20.00'}),
            'lal': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Auto-calculated', 'class': 'calc-input', 'readonly': False}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        volume_in_l = cleaned_data.get('volume_in_l')
        abv_hearts = cleaned_data.get('abv_hearts')
        lal = cleaned_data.get('lal')
        
        # Calculate LAL if volume and ABV are provided and LAL is not manually set
        if volume_in_l and abv_hearts and not lal:
            cleaned_data['lal'] = round(float(volume_in_l) * (abv_hearts / 100), 2)
        
        return cleaned_data


class TotalsRecordForm(forms.ModelForm):
    """Form for totals records"""
    class Meta:
        model = TotalsRecord
        fields = ['description', 'hearts_to_storage_location', 'hearts_abv', 'hearts_to_storage_l', 'faints_to_storage_location', 'faints_abv', 'faints_to_storage_l']
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Totals'}),
            'hearts_to_storage_location': forms.TextInput(attrs={'placeholder': 'e.g., Hearts Tank 1'}),
            'hearts_abv': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 75.00'}),
            'hearts_to_storage_l': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 100.00'}),
            'faints_to_storage_location': forms.TextInput(attrs={'placeholder': 'e.g., Faints Tank 1'}),
            'faints_abv': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 25.00'}),
            'faints_to_storage_l': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'e.g., 50.00'}),
            
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
