from django.urls import path
from . import views
from .views import CreateEmployeeCardView

app_name = 'employeeid'  

urlpatterns = [
    path('create/', CreateEmployeeCardView.as_view(), name='create_employee_card'),
    path('upload/', views.upload_employee, name='upload_employee'),
    path('bulk-upload/', views.bulk_upload_employee, name='bulk_upload'),
    path('card/<int:pk>/', views.employee_card, name='employee_card'),
    path('update/<int:pk>/', views.update_employee, name='update_employee'),
    path('delete/<int:pk>/', views.delete_employee, name='delete_employee'),
]