
from django.db import models
from django.conf import settings

class Note(models.Model):
    LEVELS = (
        ('school', 'School'),
        ('college', 'College'),
        ('university', 'University'),
    )
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True, help_text='A brief description of the note')
    file = models.FileField(upload_to='notes/')
    level = models.CharField(max_length=20, choices=LEVELS)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    