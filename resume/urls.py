from django.urls import path
from . import views
from .views import generate_pdf, upload_resume


app_name = 'resume'  

urlpatterns = [
    path('', upload_resume, name='upload_resume'),
    path('builder/', views.builder, name='builder'),
    path('pdf/<int:resume_id>/', views.generate_pdf, name='generate_pdf'),
]
