from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.conf import settings
from .models import Farmer, Farm, WeatherAlert
import requests
import json

def farmer_list(request):
    farmers = Farmer.objects.all().prefetch_related('farm_set')
    
    # Get weather data for default location
    default_location = 'New Delhi,IN'  # Default location
    weather_data = get_weather_data(default_location)
    
    # Debug print to check weather data
    print("Weather Data:", weather_data)
    
    # Get active weather alerts
    now = timezone.now()
    active_alerts = WeatherAlert.objects.filter(
        valid_from__lte=now,
        valid_until__gte=now
    ).order_by('-valid_from')
    
    context = {
        'farmers': farmers,
        'weather': weather_data,
        'location': default_location,
        'active_alerts': active_alerts,
        'now': now,
    }
    return render(request, 'farm/farmer_list.html', context)

def add_farmer(request):
    if request.method == 'POST':
        name = request.POST['name']
        village = request.POST['village']
        phone = request.POST['phone']
        land_area = float(request.POST['land_area'])
        crop = request.POST['crop']
        sowing_date = request.POST['sowing_date']

        farmer = Farmer.objects.create(name=name, village=village, phone=phone)
        Farm.objects.create(
            farmer=farmer, 
            khet_area=land_area,
            phasal_name=crop,
            bowaai_date=sowing_date
        )
        return redirect('farmer_list')
    return render(request, 'farm/farmer_form.html')


def get_weather_data(location):
    """Helper function to fetch weather data from OpenWeatherMap API"""
    # Sample data for testing when API key is not available
    sample_data = {
        'weather': [{
            'main': 'Clear', 
            'description': 'clear sky', 
            'icon': '01d'
        }],
        'main': {
            'temp': 28.5,
            'temp_min': 26,
            'temp_max': 32,
            'humidity': 65,
            'pressure': 1012
        },
        'wind': {'speed': 3.1, 'deg': 270},
        'visibility': 10000,
        'dt': int(timezone.now().timestamp()),
        'sys': {
            'sunrise': int(timezone.now().replace(hour=6, minute=0, second=0).timestamp()),
            'sunset': int(timezone.now().replace(hour=18, minute=30, second=0).timestamp()),
            'country': 'IN'
        },
        'name': 'New Delhi',
        'coord': {'lat': 28.6139, 'lon': 77.2090},
        'timezone': 19800,
        'id': 1261481,
        'cod': 200
    }
    
    try:
        api_key = getattr(settings, 'OPENWEATHER_API_KEY', None)
        if not api_key:
            print("Warning: OPENWEATHER_API_KEY is not set. Using sample weather data.")
            return sample_data
            
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': location,
            'appid': api_key,
            'units': 'metric',
            'lang': 'hi'  # Hindi language support
        }
        
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        print("Using sample weather data instead.")
        return sample_data


def weather_dashboard(request):
    """View for displaying weather dashboard"""
    location = request.GET.get('location', 'New Delhi,IN')
    weather_data = get_weather_data(location)
    
    # Get active weather alerts
    now = timezone.now()
    active_alerts = WeatherAlert.objects.filter(
        valid_from__lte=now,
        valid_until__gte=now
    ).order_by('-valid_from')
    
    # If no active alerts, create some sample alerts for demonstration
    if not active_alerts.exists():
        from datetime import timedelta
        from django.utils import timezone
        
        # Create sample alerts
        sample_alerts = [
            {
                'title': 'तेज हवाओं की चेतावनी',
                'description': 'आज शाम 5 बजे से रात 10 बजे तक 40-50 किमी/घंटा की रफ्तार से तेज हवाएं चलने की संभावना है। कृपया सावधान रहें।',
                'severity': 'medium',
                'valid_from': timezone.now() - timedelta(hours=2),
                'valid_until': timezone.now() + timedelta(hours=8)
            },
            {
                'title': 'गर्मी की लहर',
                'description': 'अगले 3 दिनों तक तापमान 42-45 डिग्री सेल्सियस तक पहुंचने की संभावना है। पर्याप्त मात्रा में पानी पिएं और धूप से बचें।',
                'severity': 'high',
                'valid_from': timezone.now() - timedelta(hours=1),
                'valid_until': timezone.now() + timedelta(days=3)
            }
        ]
        
        # Add sample alerts to context
        context = {
            'weather': weather_data,
            'location': location,
            'active_alerts': sample_alerts,
            'using_sample_alerts': True  # Flag to indicate using sample data
        }
    else:
        context = {
            'weather': weather_data,
            'location': location,
            'active_alerts': active_alerts,
            'using_sample_alerts': False
        }
    return render(request, 'farm/weather_dashboard.html', context)


def weather_alert_detail(request, alert_id):
    """View for displaying detailed weather alert"""
    alert = get_object_or_404(WeatherAlert, id=alert_id)
    return render(request, 'farm/weather_alert_detail.html', {'alert': alert})
