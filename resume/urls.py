from django.urls import path
from . import views
from .views import generate_pdf, upload_resume, builder, simple_builder, test_pdf

app_name = 'resume'

urlpatterns = [
    path('', upload_resume, name='upload_resume'),
    path('builder/', builder, name='builder'),
    path('builder/<str:template_type>/', builder, name='builder_template'),
    path('builder/<str:template_type>/<int:resume_id>/', builder, name='builder_template_with_id'),
    path('simple/', simple_builder, name='simple_builder'),
    path('simple/<int:resume_id>/', simple_builder, name='edit_simple_resume'),
    path('pdf/<int:resume_id>/', generate_pdf, name='generate_pdf'),
    path('pdf/<str:template_type>/<int:resume_id>/', generate_pdf, name='generate_pdf_template'),
    path('preview/', views.preview_resume, name='preview'),
    path('test-pdf/', test_pdf, name='test_pdf'),
]
