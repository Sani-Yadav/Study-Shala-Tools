import random
import string
from django.db import models
from django.db.models import Max

def get_next_id():
    """Helper function to get the next ID number"""
    from django.apps import apps
    IDCard = apps.get_model('id_card_app', 'IDCard')
    max_id = IDCard.objects.aggregate(Max('id'))['id__max']
    return 1 if max_id is None else max_id + 1

class IDCard(models.Model):
    name = models.CharField(max_length=100)
    id_no = models.CharField(max_length=50, unique=True, blank=True)
    mobile = models.CharField(max_length=20)
    issued_date = models.DateField(auto_now_add=True)
    
    # ImageField for the photo, uploads to media/photos/
    photo = models.ImageField(upload_to='photos/')
    
    # ImageField for the digital signature, uploads to media/signatures/
    digital_signature = models.ImageField(upload_to='signatures/')
    
    # Auto set the date when the object is first created
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Only set the ID number if this is a new record
        if not self.id_no:
            self.id_no = f"{get_next_id():04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.id_no}"
        
    class Meta:
        db_table = 'political_id_idcard'