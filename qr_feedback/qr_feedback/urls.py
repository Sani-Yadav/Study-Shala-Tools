from django.contrib import admin
from django.urls import path
from qr_feedback.feedback.views import create_form, generate_qr, submit_feedback

app_name = 'feedback'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', create_form, name='create_form'),
    path('qr/<slug:slug>/', generate_qr, name='generate_qr'),
    path('form/<slug:slug>/', submit_feedback, name='submit_feedback'),
]