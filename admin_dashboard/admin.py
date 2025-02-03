from django.contrib import admin
from .models import AdminAccountDetails

@admin.register(AdminAccountDetails)
class AdminAccountDetailsAdmin(admin.ModelAdmin):
    list_display = ['account_type', 'account_number', 'account_name']
    
    def save_model(self, request, obj, form, change):
        # Check if account type already exists
        try:
            existing = AdminAccountDetails.objects.get(account_type=obj.account_type)
            # Update existing record
            existing.account_number = obj.account_number
            existing.account_name = obj.account_name
            existing.additional_info = obj.additional_info
            existing.save()
        except AdminAccountDetails.DoesNotExist:
            # Create new record
            obj.save()
