from django.db import models
from django.conf import settings
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.urls import reverse

class IDCard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='id_cards')
    Full_Name = models.CharField(max_length=20, unique=True)
    student_id = models.CharField(max_length=50, unique=True, verbose_name='Student ID', default='', blank=True)
    college = models.CharField(max_length=100, verbose_name='College/School', default='', blank=True)
    course = models.CharField(max_length=50, verbose_name='Course', default='', blank=True)
    year = models.CharField(max_length=20, verbose_name='Year/Batch', default='', blank=True)
    contact_number = models.CharField(max_length=15, verbose_name='Contact Number', default='', blank=True)
    address = models.TextField(blank=True, null=True, verbose_name='Address')
    dob = models.DateField(blank=True, null=True, verbose_name='Date of Birth')
    issue_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='id_cards/', null=True, blank=True)
    qr_code = models.ImageField(upload_to='id_cards/qr_codes/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"ID Card: {self.Full_Name} - {self.user.username if self.user else 'No User'}"
    
    def save(self, *args, **kwargs):
        # Generate QR code if it doesn't exist
        if not self.qr_code:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            # Add data to QR code (only include essential information)
            qr_data = f"ID:{self.student_id}|Name:{self.Full_Name}|Course:{self.course}|Year:{self.year}"
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # Create QR code image
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            self.qr_code.save(f'qr_{self.student_id}.png', File(buffer), save=False)
            
        super().save(*args, **kwargs)
