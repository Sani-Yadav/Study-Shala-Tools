# idcard/urls.py
from django.urls import path
from .views import create_id_card, id_card_view, update_id_card, bulk_upload_id_cards, delete_id_card

app_name = 'idcard'  # Yeh line add karo

urlpatterns = [
    path('create/', create_id_card, name='create_id_card'),
    path('view/', id_card_view, name='id_card_view'),
    path('update/<int:card_id>/', update_id_card, name='update_id_card'),
    path('delete/<int:card_id>/', delete_id_card, name='delete_id_card'),
    path('bulk-upload/', bulk_upload_id_cards, name='bulk_upload_id_cards'),
]