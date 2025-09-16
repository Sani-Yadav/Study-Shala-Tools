from asn1crypto.core import Null
from django.db import models
from django.conf import settings

class Resume(models.Model):
    # User who owns this resume
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resume', null=True, blank=True)
    
    #  Personal Info
    profile_image = models.ImageField(upload_to='resumes/profile_images/', blank=True, null=True)
    full_name = models.CharField(max_length=100,blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True, verbose_name='Job Title/Position')
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20,blank=True, null=True)
    address = models.TextField(blank=True, null=True, help_text='Your full address')
    location = models.CharField(max_length=100, blank=True, null=True, help_text='City, Country')
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)

    #  Summary & Skills
    summary = models.TextField(blank=True, null=True)
    technical_skills = models.CharField(max_length=300, blank=True, null=True)
    soft_skills = models.CharField(max_length=300, blank=True, null=True)
    languages = models.CharField(max_length=200, blank=True, null=True)
    hobbies = models.CharField(max_length=200, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'resume'
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.full_name}'s Resume"


class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experiences')
    job_title = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'resume'

    def __str__(self):
        return f"{self.job_title or ''} at {self.company or ''}"


class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education_entries')
    degree = models.CharField(max_length=100, blank=True, null=True)
    institution = models.CharField(max_length=100, blank=True, null=True)
    year = models.CharField(max_length=20, blank=True, null=True)
    result = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        app_label = 'resume'

    def __str__(self):
        return f"{self.degree or ''} at {self.institution or ''}"


class Project(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    tech_stack = models.CharField(max_length=100, blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)

    class Meta:
        app_label = 'resume'

    def __str__(self):
        return self.title or "Untitled Project"


class Certification(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='certifications')
    title = models.CharField(max_length=100, blank=True, null=True)
    platform = models.CharField(max_length=100, blank=True, null=True)
    year = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        app_label = 'resume'

    def __str__(self):
        return self.title or "Certification"


class Achievement(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='achievements')
    description = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'resume'

    def __str__(self):
        return f"Achievement for {self.resume.full_name}"


class Reference(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='references')
    name = models.CharField(max_length=100, blank=True, null=True)
    relationship = models.CharField(max_length=100, blank=True, null=True)
    contact_info = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        app_label = 'resume'

    def __str__(self):
        return f"Reference: {self.name or ''}"
