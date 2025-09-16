from django.urls import path
from .views import satellite_position_view, index

app_name = 'satellite_tracker'

urlpatterns = [
    path('', index, name='index'),
    path('satellite-position/<str:satellite_id>/', satellite_position_view, name='satellite_position'),
    path('satellite-position/', satellite_position_view, name='satellite_position_default'),  # For backward compatibility
]
