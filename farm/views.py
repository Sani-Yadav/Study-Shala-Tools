from django.shortcuts import render, redirect
from .models import Farmer, Farm
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import WeatherAlert
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def farmer_list(request):
    farmers = Farmer.objects.all().prefetch_related('farm_set')
    return render(request, 'farm/farmer_list.html', {'farmers': farmers})

def add_farmer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        village = request.POST.get('village')
        phone = request.POST.get('phone')
        land_area = float(request.POST.get('land_area', 0))
        crop = request.POST.get('crop')
        sowing_date = request.POST.get('sowing_date')

        farmer = Farmer.objects.create(name=name, village=village, phone=phone)
        Farm.objects.create(
            farmer=farmer, 
            khet_area=land_area,
            phasal_name=crop,
            bowaai_date=sowing_date
        )
        return redirect('farm:farmer_list')
    return render(request, 'farm/add_farmer.html')

def update_farmer(request, farmer_id):
    farmer = get_object_or_404(Farmer, id=farmer_id)
    farm = farmer.farm_set.first()
    
    if request.method == 'POST':
        farmer.name = request.POST.get('name', farmer.name)
        farmer.village = request.POST.get('village', farmer.village)
        farmer.phone = request.POST.get('phone', farmer.phone)
        farmer.save()
        
        if farm:
            farm.phasal_name = request.POST.get('crop', farm.phasal_name)
            farm.khet_area = float(request.POST.get('land_area', farm.khet_area))
            farm.bowaai_date = request.POST.get('sowing_date', farm.bowaai_date)
            farm.save()
        
        return redirect('farm:farmer_list')
    
    context = {
        'farmer': farmer,
        'farm': farm
    }
    return render(request, 'farm/update_farmer.html', context)

def farmer_payment(request, farmer_id):
    farmer = get_object_or_404(Farmer, id=farmer_id)
    
    if request.method == 'POST':
        # Handle payment processing here
        amount = float(request.POST.get('amount', 0))
        payment_date = request.POST.get('payment_date')
        payment_method = request.POST.get('payment_method')
        
        # Create payment record (you'll need to create a Payment model)
        # Payment.objects.create(
        #     farmer=farmer,
        #     amount=amount,
        #     payment_date=payment_date,
        #     payment_method=payment_method
        # )
        
        return redirect('farm:farmer_list')
    
    context = {
        'farmer': farmer
    }
    return render(request, 'farm/farmer_payment.html', context)

    return redirect('farm:farmer_list')
    return render(request, 'farm/farmer_form.html')


def get_weather_data(location):
    """Helper to fetch weather data from OpenWeatherMap."""
    try:
        api_key = getattr(settings, 'OPENWEATHER_API_KEY', None)
        if not api_key:
            logger.error("OpenWeatherMap API key not found in settings")
            return None
            
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': location, 
            'appid': api_key, 
            'units': 'metric', 
            'lang': 'hi'
        }
        
        logger.info(f"Fetching weather for {location} with API key: {api_key[:5]}...")
        resp = requests.get(base_url, params=params)
        resp.raise_for_status()
        
        weather_data = resp.json()
        logger.info(f"Weather data received: {weather_data}")
        return weather_data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather data: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Response status: {e.response.status_code}")
            logger.error(f"Response content: {e.response.text}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        
    return None


def weather_dashboard(request):
    location = request.GET.get('location', 'New Delhi,IN')
    logger.info(f"Weather dashboard requested for location: {location}")
    
    # Get weather data
    weather_data = get_weather_data(location)
    
    # Get current time in the correct timezone
    now = timezone.now()
    
    # Get active alerts
    active_alerts = []
    try:
        # First check if the WeatherAlert table exists
        from django.db import connection
        if 'farm_weatheralert' in connection.introspection.table_names():
            active_alerts = WeatherAlert.objects.filter(
                valid_from__lte=now,
                valid_until__gte=now
            ).order_by('-valid_from')
            logger.info(f"Found {len(active_alerts)} active alerts")
        else:
            logger.warning("WeatherAlert table does not exist in the database")
    except Exception as e:
        logger.error(f"Error fetching weather alerts: {str(e)}")
    
    context = {
        'weather': weather_data,
        'location': location,
        'active_alerts': active_alerts
    }
    
    logger.info(f"Rendering weather dashboard with context: {context}")
    return render(request, 'farm/weather_dashboard.html', context)


def weather_alert_detail(request, alert_id):
    alert = get_object_or_404(WeatherAlert, id=alert_id)
    return render(request, 'farm/weather_alert_detail.html', {'alert': alert})


def farmer_detail(request, farmer_id):
    """View for displaying detailed information about a specific farmer"""
    farmer = get_object_or_404(Farmer, id=farmer_id)
    farm = farmer.farm_set.first()
    
    # Get weather data for the farmer's location
    weather_data = get_weather_data(farmer.village or 'New Delhi,IN')
    
    context = {
        'farmer': farmer,
        'farm': farm,
        'weather': weather_data,
    }
    return render(request, 'farm/farmer_detail.html', context)
