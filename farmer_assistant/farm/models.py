from django.db import models
from django.utils import timezone

class Farmer(models.Model):
    name = models.CharField(
        max_length=100, 
        verbose_name="Kisan ka Naam (Name)"
    )
    village = models.CharField(
        max_length=100, 
        verbose_name="Gaav (Village)"
    )
    phone = models.CharField(
        max_length=15, 
        verbose_name="Mobile Number"
    )

    class Meta:
        app_label = 'farm'

    def __str__(self):
        return f"{self.name} ({self.village})"


class Farm(models.Model):
    farmer = models.ForeignKey(
        Farmer, 
        on_delete=models.CASCADE, 
        verbose_name="Kisan (Farmer)"
    )
    khet_area = models.FloatField(
        help_text="Khet ka area (acres mein)", 
        verbose_name="Khet ka Area"
    )
    phasal_name = models.CharField(
        max_length=100, 
        verbose_name="Phasal ka Naam (Crop)"
    )
    bowaai_date = models.DateField(
        verbose_name="Bone ki Date (Sowing Date)"
    )

    class Meta:
        app_label = 'farm'

    def __str__(self):
        return f"{self.farmer.name}'s {self.phasal_name} farm ({self.khet_area} acres)"


class WeatherAlert(models.Model):
    ALERT_TYPES = [
        ('rain', 'बारिश (Rain)'),
        ('storm', 'तूफान (Storm)'),
        ('hail', 'ओलावृष्टि (Hailstorm)'),
        ('drought', 'सूखा (Drought)'),
        ('heatwave', 'लू (Heatwave)'),
        ('other', 'अन्य (Other)'),
    ]
    
    alert_type = models.CharField(
        max_length=20,
        choices=ALERT_TYPES,
        verbose_name="अलर्ट प्रकार (Alert Type)"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="शीर्षक (Title)"
    )
    description = models.TextField(
        verbose_name="विवरण (Description)"
    )
    severity = models.CharField(
        max_length=20,
        choices=[
            ('low', 'कम (Low)'),
            ('medium', 'मध्यम (Medium)'),
            ('high', 'उच्च (High)'),
        ],
        default='medium',
        verbose_name="गंभीरता (Severity)"
    )
    valid_from = models.DateTimeField(
        default=timezone.now,
        verbose_name="प्रभावी तिथि (Valid From)"
    )
    valid_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="समाप्ति तिथि (Valid Until)"
    )
    location = models.CharField(
        max_length=100,
        default='All Regions',
        verbose_name="स्थान (Location)"
    )
    
    def __str__(self):
        return f"[{self.get_alert_type_display()}] {self.title}"
    
    class Meta:
        ordering = ['-valid_from']
        verbose_name = 'मौसम चेतावनी (Weather Alert)'
        verbose_name_plural = 'मौसम चेतावनियाँ (Weather Alerts)'
