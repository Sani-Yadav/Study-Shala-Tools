from django.urls import path
from . import views

app_name = 'sarkarisahyogi'  # This is the app namespace

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('apply-job/', views.apply_job, name='apply_job'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
