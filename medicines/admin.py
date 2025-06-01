from django.contrib import admin
from .models import Medicine


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'batch_number', 'expiry_date', 'quantity', 'storage_location', 'expiry_status')
    list_filter = ('storage_condition', 'date_added')
    search_fields = ('name', 'batch_number', 'description')
    date_hierarchy = 'expiry_date'
    readonly_fields = ('date_added', 'last_updated')
    
    def expiry_status(self, obj):
        status = obj.expiry_status()
        if status == 'expired' or status == 'expiring_soon':
            return f'❌ {obj.days_until_expiry()} days'
        elif status == 'near_expiry':
            return f'⚠️ {obj.days_until_expiry()} days'
        else:
            return f'✅ {obj.days_until_expiry()} days'
    
    expiry_status.short_description = 'Expiry Status'
