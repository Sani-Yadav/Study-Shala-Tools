
from django.urls import path
from . import views
from . import test_view

app_name = 'media_downloader'

urlpatterns = [
    path('', views.home, name='home'),
    path('test/', test_view.test_view, name='test_view'),
    path('download-media/', views.download_media, name='download_media'),
    path('movies/search/', views.search_movies, name='search_movies'),
    path('movies/<str:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movies/<str:movie_id>/download/', views.download_movie, name='download_movie'),
]
