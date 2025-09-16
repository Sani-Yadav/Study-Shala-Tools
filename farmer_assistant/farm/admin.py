from django.contrib import admin
from .models import Farmer, Farm, WeatherAlert

admin.site.register(Farmer)
admin.site.register(Farm)
admin.site.register(WeatherAlert)
