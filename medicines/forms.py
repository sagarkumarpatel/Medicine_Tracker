from django import forms
from .models import Medicine
from django.utils import timezone
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'batch_number', 'expiry_date', 'quantity', 
                 'storage_location', 'storage_condition', 'description', 'barcode']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date().isoformat()}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean_expiry_date(self):
        expiry_date = self.cleaned_data.get('expiry_date')
        if expiry_date and expiry_date < timezone.now().date():
            raise forms.ValidationError("Expiry date cannot be in the past.")
        return expiry_date
    
    def save(self, commit=True):
        medicine = super().save(commit=False)
        
        # Generate QR code if we have a medicine ID (for updates)
        if medicine.pk and not medicine.qr_code:
            self.generate_qr_code(medicine)
            
        if commit:
            medicine.save()
        return medicine
    
    def generate_qr_code(self, medicine):
        # QR code data - can include more details as needed
        qr_data = f"Name: {medicine.name}\nBatch: {medicine.batch_number}\nExpiry: {medicine.expiry_date}\nID: {medicine.pk}"
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Create PIL image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to model field
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        filename = f"medicine_{medicine.pk}_qr.png"
        medicine.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)


class MedicineSearchForm(forms.Form):
    search_query = forms.CharField(required=False, label="Search", 
                                  widget=forms.TextInput(attrs={'placeholder': 'Search by name, batch number...', 'class': 'form-control'}))

    expiry_status = forms.ChoiceField(choices=[
        ('', 'All Status'),
        ('expired', 'Expired'),
        ('expiring_soon', 'Expiring in 7 days'),
        ('near_expiry', 'Expiring in 30 days'),
        ('safe', 'Safe'),
    ], required=False, widget=forms.Select(attrs={'class': 'form-select'}))