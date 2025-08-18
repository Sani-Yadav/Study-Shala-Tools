from django.urls import path
from . import views

app_name = 'employeeid'  

urlpatterns = [
    path('upload/', views.upload_employee, name='upload_employee'),
    path('card/<int:pk>/', views.employee_card, name='employee_card'),
    path('update/<int:pk>/', views.update_employee, name='update_employee'),
]