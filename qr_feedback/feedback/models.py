from django.db import models

class FeedbackForm(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    owner_email = models.EmailField('Form Owner Email', help_text='Email where you want to receive feedback notifications')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class FeedbackResponse(models.Model):
    form = models.ForeignKey(FeedbackForm, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.CharField(max_length=20, choices=[
        ('Excellent', 'Excellent'),
        ('Good', 'Good'),
        ('Average', 'Average'),
        ('Poor', 'Poor')
    ])
    suggestion = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)