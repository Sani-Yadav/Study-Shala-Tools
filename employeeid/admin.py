from django.contrib import admin
from .models import Employee
from django.utils.html import format_html

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'employee_id',
        'designation',
        'department',
        'company',
        'email',
        'join_date',
        'qr_preview'
    )
    search_fields = ('full_name', 'employee_id', 'email')
    list_filter = ('department', 'company', 'join_date')

    def qr_preview(self, obj):
        if obj.qr_code:
            return format_html('<img src="{}" width="50" height="50"/>', obj.qr_code.url)
        return "No QR"
    qr_preview.short_description = 'QR Code'
