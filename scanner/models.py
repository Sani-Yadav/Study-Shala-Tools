from django.db import models

# Create your models here.

class ScannedNote(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='notes_images/')
    extracted_text = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to='pdfs/', blank=True)

    def __str__(self):
        return self.title
