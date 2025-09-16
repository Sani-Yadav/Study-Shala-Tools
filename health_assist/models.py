from django.db import models
from django.utils import timezone 
class Hospital(models.Model):
    name = models.CharField(max_length=200, verbose_name='Hospital Name')
    state = models.CharField(max_length=100, verbose_name='State', default='Uttar Pradesh')
    district = models.CharField(max_length=100, verbose_name='District', default='Sultanpur')
    phone = models.CharField(max_length=15, verbose_name='Phone Number')
    is_24x7 = models.BooleanField(default=False, verbose_name='24x7 Available')
    address = models.TextField(blank=True, null=True, verbose_name='Full Address')
    latitude = models.FloatField(null=True, blank=True, verbose_name='Latitude')
    longitude = models.FloatField(null=True, blank=True, verbose_name='Longitude')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        ordering = ['name'] 
        verbose_name = 'Hospital'
        verbose_name_plural = 'Hospitals'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['state']),
            models.Index(fields=['district']),
        ]

    def __str__(self):
        return f"{self.name}, {self.district}"

class EmergencyContact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

