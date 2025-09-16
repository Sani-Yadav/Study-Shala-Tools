from django.core.management.base import BaseCommand
from django.utils import timezone
from farm.models import WeatherAlert
from datetime import timedelta

class Command(BaseCommand):
    help = 'Adds sample weather alerts for demonstration purposes'

    def handle(self, *args, **options):
        # Delete any existing sample alerts
        WeatherAlert.objects.all().delete()
        
        now = timezone.now()
        
        # Sample alerts in Hindi
        sample_alerts = [
            {
                'title': 'तेज हवाओं की चेतावनी',
                'description': 'आज शाम 5 बजे से रात 10 बजे तक 40-50 किमी/घंटा की रफ्तार से तेज हवाएं चलने की संभावना है। कृपया सावधान रहें।',
                'alert_type': 'storm',
                'severity': 'medium',
                'valid_from': now - timedelta(hours=2),
                'valid_until': now + timedelta(hours=8),
                'location': 'दिल्ली और आसपास के इलाके'
            },
            {
                'title': 'गर्मी की लहर',
                'description': 'अगले 3 दिनों तक तापमान 42-45 डिग्री सेल्सियस तक पहुंचने की संभावना है। पर्याप्त मात्रा में पानी पिएं और धूप से बचें।',
                'alert_type': 'heatwave',
                'severity': 'high',
                'valid_from': now - timedelta(hours=1),
                'valid_until': now + timedelta(days=3),
                'location': 'उत्तरी भारत'
            },
            {
                'title': 'भारी बारिश की चेतावनी',
                'description': 'कल दोपहर से अगले 24 घंटों तक भारी बारिश का अनुमान है। कृपया आवश्यक सावधानी बरतें।',
                'alert_type': 'rain',
                'severity': 'high',
                'valid_from': now + timedelta(hours=6),
                'valid_until': now + timedelta(hours=30),
                'location': 'पूर्वी भारत'
            }
        ]
        
        # Create alerts
        for alert_data in sample_alerts:
            WeatherAlert.objects.create(**alert_data)
        
        self.stdout.write(self.style.SUCCESS('Successfully added sample weather alerts'))
