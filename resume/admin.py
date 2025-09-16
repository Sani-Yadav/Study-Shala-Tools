from django.contrib import admin
from .models import (
    Education, 
    Experience, 
    Project, 
    Resume, 
    Certification,
    Achievement,
    Reference
)


# Register your models here.
admin.site.register(Resume)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Project)
admin.site.register(Certification)
admin.site.register(Achievement)
admin.site.register(Reference)
