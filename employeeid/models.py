from django.db import models

# Create your models here.
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image

class Employee(models.Model):
    full_name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50, unique=True)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    join_date = models.DateField()
    profile_image = models.ImageField(upload_to='employee_photos/')
    qr_code = models.ImageField(upload_to='employee_qr/', blank=True)

    class Meta:
        app_label = 'employeeid'
        db_table = 'employeeid_employee'
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def save(self, *args, **kwargs):
        qr_data = f"{self.full_name} | {self.employee_id} | {self.designation} | {self.email}"
        qr_img = qrcode.make(qr_data)
        qr_io = BytesIO()
        qr_img.save(qr_io, format='PNG')
        self.qr_code.save(f'{self.employee_id}_qr.png', File(qr_io), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
