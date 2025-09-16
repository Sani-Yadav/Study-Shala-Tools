from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_profile')
    full_name = models.CharField(max_length=200)
    dob = models.DateField()
    address = models.TextField()
    photo = models.ImageField(upload_to='photos/')
    
    def __str__(self):
        return f"{self.full_name}'s job profile"

class JobApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    applied_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')
