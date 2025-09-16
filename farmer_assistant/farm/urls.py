from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'farm'

urlpatterns = [
    path('', views.farmer_list, name='farmer_list'),
    path('add/', views.add_farmer, name='add_farmer'),
    path('add_farmer/', views.add_farmer, name='add_farmer_alt'),  # Alternative URL for form submission
    # Weather URLs
    path('weather/', views.weather_dashboard, name='weather_dashboard'),
    path('weather/alert/<int:alert_id>/', views.weather_alert_detail, name='weather_alert_detail'),
]
