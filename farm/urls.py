app_name = 'farm'

from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='farmers/'), name='home'),
    path('farmers/', views.farmer_list, name='farmer_list'),
    path('farmer/add/', views.add_farmer, name='add_farmer'),
    path('farmer/update/<int:farmer_id>/', views.update_farmer, name='update_farmer'),
    path('farmer/payment/<int:farmer_id>/', views.farmer_payment, name='farmer_payment'),
    
    # Farmer detail URL
    path('farmer/<int:farmer_id>/', views.farmer_detail, name='farmer_detail'),
    
    # Weather URLs
    path('weather/', views.weather_dashboard, name='weather_dashboard'),
    path('weather/alert/<int:alert_id>/', views.weather_alert_detail, name='weather_alert_detail'),
]
