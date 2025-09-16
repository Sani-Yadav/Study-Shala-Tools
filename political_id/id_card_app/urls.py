from django.urls import path
from . import views

app_name = 'id_card_app'  # This is the app's namespace

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_id_card, name='create_id_card'),
    path('show/<int:pk>/', views.show_id_card, name='show_id_card'),
]