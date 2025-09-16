from django.contrib import admin
from .models import Farmer, Farm, WeatherAlert

class WeatherAlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'alert_type', 'severity', 'valid_from', 'valid_until')
    list_filter = ('alert_type', 'severity')
    search_fields = ('title', 'description')
    date_hierarchy = 'valid_from'

admin.site.register(Farmer)
admin.site.register(Farm)
admin.site.register(WeatherAlert, WeatherAlertAdmin)
