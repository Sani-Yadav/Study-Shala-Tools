from django.urls import path
from . import views

app_name = 'scanner'
 
urlpatterns = [
    path('', views.scan_note, name='scan_note'),
    path('note/<int:pk>/', views.note_detail, name='note_detail'),
] 