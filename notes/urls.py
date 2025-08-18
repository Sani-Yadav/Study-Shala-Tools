app_name = 'notes'
from django.urls import path
from . import views

urlpatterns = [
    path('', views.notes_list, name='notes_list'),
    path('<int:note_id>/', views.note_detail, name='note_detail'),
    path('upload/', views.upload_note, name='upload_note'),
    path('my-notes/', views.my_notes, name='my_notes'),
    path('<int:note_id>/delete/', views.delete_note, name='delete_note'),
]