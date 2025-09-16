import os
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studyshala.settings')
django.setup()

from farm.models import WeatherAlert

def check_alerts():
    # Check if we can connect to the database
    try:
        count = WeatherAlert.objects.count()
        print(f"Found {count} weather alerts in the database")
        
        if count > 0:
            print("\nSample alerts:")
            for alert in WeatherAlert.objects.all()[:3]:
                print(f"\nTitle: {alert.title}")
                print(f"Type: {alert.get_alert_type_display()}")
                print(f"Severity: {alert.get_severity_display()}")
                print(f"Valid from: {alert.valid_from}")
                print(f"Valid until: {alert.valid_until}")
                print(f"Location: {alert.location}")
                print(f"Description: {alert.description[:100]}..." if len(alert.description) > 100 else f"Description: {alert.description}")
        else:
            print("No alerts found in the database.")
            
    except Exception as e:
        print(f"Error accessing database: {e}")

def add_sample_alerts():
    """Add sample weather alerts to the database"""
    now = timezone.now()
    
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
    
    print("Successfully added sample weather alerts")

if __name__ == "__main__":
    # First check if we have any alerts
    count = WeatherAlert.objects.count()
    
    if count == 0:
        print("No alerts found. Adding sample alerts...")
        add_sample_alerts()
    
    # Now check and display alerts
    check_alerts()
