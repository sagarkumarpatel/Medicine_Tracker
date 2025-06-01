from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
import datetime


class MedicineCategory(models.Model):
    """Model for medicine categories (e.g., tablets, syrups, injections)"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Medicine Categories"
    
    def __str__(self):
        return self.name


class Medicine(models.Model):
    """Model for medicine details"""
    STORAGE_CHOICES = [
        ('room_temp', 'Room Temperature'),
        ('refrigerated', 'Refrigerated'),
        ('freezer', 'Freezer'),
        ('cool_dry', 'Cool and Dry Place'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    batch_number = models.CharField(max_length=100)

    expiry_date = models.DateField()
    quantity = models.PositiveIntegerField(default=1)
    storage_location = models.CharField(max_length=100, blank=True, null=True)
    storage_condition = models.CharField(max_length=20, choices=STORAGE_CHOICES, default='room_temp')
    description = models.TextField(blank=True, null=True)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medicines')
    
    def __str__(self):
        return f"{self.name} - {self.batch_number}"
    
    def get_absolute_url(self):
        return reverse('medicine-detail', kwargs={'pk': self.pk})
    
    def days_until_expiry(self):
        """Calculate days until expiry"""
        today = timezone.now().date()
        delta = self.expiry_date - today
        return delta.days
    
    def expiry_status(self):
        """Return expiry status for color coding"""
        days = self.days_until_expiry()
        if days < 0:
            return 'expired'  # Red
        elif days <= 7:
            return 'expiring_soon'  # Red
        elif days <= 30:
            return 'near_expiry'  # Yellow
        else:
            return 'safe'  # Green
