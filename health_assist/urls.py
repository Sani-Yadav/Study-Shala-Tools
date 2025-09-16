from django.urls import path
from .views import health_home, HospitalListView, get_districts

app_name = 'health_assist'  # Define the app's namespace

urlpatterns = [
    path('', health_home, name='health_home'),
    path('hospitals/', HospitalListView.as_view(), name='hospital_list'),
    path('api/districts/', get_districts, name='get_districts'),
]
