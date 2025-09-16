from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
User = get_user_model()
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
import os

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='folder')
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Movie(models.Model):
    QUALITY_CHOICES = [
        ('HD', 'HD'),
        ('Full HD', 'Full HD'),
        ('4K', '4K'),
    ]
    
    LANGUAGE_CHOICES = [
        ('Hindi', 'Hindi'),
        ('English', 'English'),
        ('Tamil', 'Tamil'),
        ('Telugu', 'Telugu'),
        ('Other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    release_year = models.PositiveIntegerField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    quality = models.CharField(max_length=10, choices=QUALITY_CHOICES, default='HD')
    thumbnail = models.ImageField(upload_to='thumbnails/')
    banner = models.ImageField(upload_to='banners/')
    video_url = models.URLField()
    categories = models.ManyToManyField(Category, related_name='movies')
    imdb_rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)], null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.release_year})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.release_year}")
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return f'/movie/{self.slug}/'

class WebSeries(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    release_year = models.PositiveIntegerField()
    language = models.CharField(max_length=20, choices=Movie.LANGUAGE_CHOICES)
    thumbnail = models.ImageField(upload_to='series_thumbnails/')
    banner = models.ImageField(upload_to='series_banners/')
    categories = models.ManyToManyField(Category, related_name='web_series')
    imdb_rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)], null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Web Series'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.release_year})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.release_year}")
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return f'/series/{self.slug}/'

class Episode(models.Model):
    web_series = models.ForeignKey(WebSeries, on_delete=models.CASCADE, related_name='episodes')
    title = models.CharField(max_length=200)
    episode_number = models.PositiveIntegerField()
    season_number = models.PositiveIntegerField(default=1)
    video_url = models.URLField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    is_free = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['season_number', 'episode_number']
        unique_together = ('web_series', 'season_number', 'episode_number')
    
    def __str__(self):
        return f"{self.web_series.title} - S{self.season_number:02d}E{self.episode_number:02d}: {self.title}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='downloader_profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    subscription_expiry = models.DateField(blank=True, null=True)
    is_premium = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s downloader profile"

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField(help_text="Duration in days")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - ₹{self.price}"

class Download(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=20, choices=[('movie', 'Movie'), ('episode', 'Episode')])
    content_id = models.PositiveIntegerField()
    downloaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-downloaded_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.content_type} #{self.content_id}"

class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=20, choices=[('movie', 'Movie'), ('episode', 'Episode')])
    content_id = models.PositiveIntegerField()
    watched_at = models.DateTimeField(auto_now_add=True)
    duration_watched = models.PositiveIntegerField(help_text="Duration watched in seconds")
    
    class Meta:
        verbose_name_plural = 'Watch History'
        ordering = ['-watched_at']
    
    def __str__(self):
        return f"{self.user.username} watched {self.content_type} #{self.content_id}"
