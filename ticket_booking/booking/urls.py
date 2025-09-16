from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("search/", views.search, name="search"),
    path("book/<int:id>/", views.book_ticket, name="book_ticket"),
    path('confirm_seats/<int:id>/', views.confirm_seats, name='confirm_seats'),
]
