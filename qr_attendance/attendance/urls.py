from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('generate/', views.generate_attendance_qr, name='generate_qr'),
    path('mark/', views.attendance_mark, name='mark_attendance'),
    path('download/', views.download_attendance_records, name='download_all_attendance'),
    path('download/<str:session_id>/', views.download_attendance_records, name='download_attendance'),
]
