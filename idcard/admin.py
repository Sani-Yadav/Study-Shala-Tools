from django.contrib import admin
from .models import IDCard

@admin.register(IDCard)
class IDCardAdmin(admin.ModelAdmin):
    list_display = ('Full_Name', 'user', 'issue_date', 'expiry_date', 'is_active')
    list_filter = ('is_active', 'issue_date')
    search_fields = ('Full_Name', 'user__username', 'user__email')
    readonly_fields = ('issue_date',)
