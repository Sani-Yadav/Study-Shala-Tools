import os
import sys
import django
from datetime import datetime, timedelta

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studyshala.settings')
django.setup()

from farm.models import WeatherAlert

def check_database():
    try:
        # Test database connection
        count = WeatherAlert.objects.count()
        print(f"Connected to database. Found {count} weather alerts.")
        return True
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return False

def add_sample_alerts():
    now = django.utils.timezone.now()
    
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
        }
    ]
    
    try:
        # Delete existing alerts
        WeatherAlert.objects.all().delete()
        
        # Create new alerts
        for alert_data in sample_alerts:
            WeatherAlert.objects.create(**alert_data)
            
        print("Successfully added sample weather alerts")
        return True
    except Exception as e:
        print(f"Error adding sample alerts: {e}")
        return False

if __name__ == "__main__":
    print("Testing database connection...")
    if check_database():
        print("Adding sample weather alerts...")
        if add_sample_alerts():
            # Display the added alerts
            print("\nCurrent weather alerts:")
            print("-" * 50)
            for alert in WeatherAlert.objects.all():
                print(f"\nTitle: {alert.title}")
                print(f"Type: {alert.alert_type}")
                print(f"Severity: {alert.severity}")
                print(f"Valid from: {alert.valid_from}")
                print(f"Valid until: {alert.valid_until}")
                print(f"Location: {alert.location}")
                print(f"Description: {alert.description}")
                print("-" * 50)
