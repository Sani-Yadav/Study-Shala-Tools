from django.contrib import admin
from .models import UserProfile, JobApplication

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(JobApplication)
