import json
import os
import uuid
import yt_dlp
import mimetypes
import requests
import socket
import urllib3
from urllib3.exceptions import MaxRetryError, TimeoutError
from requests.exceptions import RequestException, Timeout, ConnectionError
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

# OMDB API Configuration
OMDB_API_KEY = '5a1d5912'  # Updated OMDB API key
OMDB_BASE_URL = 'http://www.omdbapi.com/'
POSTER_BASE_URL = f'http://img.omdbapi.com/?apikey={OMDB_API_KEY}&'

# Request timeout in seconds
REQUEST_TIMEOUT = 10  # 10 seconds timeout

# Home view for /media-downloader/
def home(request):
    latest_content = {
        'movies': [],
        'series': [],
        'dramas': []
    }
    
    try:
        # Fetch latest movies
        movies_data = make_omdb_request({
            's': 'movie',
            'y': '2024',
            'type': 'movie',
            'page': 1
        })
        
        if movies_data.get('Response') == 'True':
            latest_content['movies'] = [{
                'id': m.get('imdbID'),
                'title': m.get('Title'),
                'year': m.get('Year'),
                'poster': m.get('Poster'),
                'type': m.get('Type')
            } for m in movies_data.get('Search', [])[:6]]
        
        # Fetch latest TV series
        series_data = make_omdb_request({
            's': 'series',
            'y': '2024',
            'type': 'series',
            'page': 1
        })
        
        if series_data.get('Response') == 'True':
            latest_content['series'] = [{
                'id': s.get('imdbID'),
                'title': s.get('Title'),
                'year': s.get('Year'),
                'poster': s.get('Poster'),
                'type': s.get('Type')
            } for s in series_data.get('Search', [])[:6]]
            
    except Exception as e:
        print(f"Error fetching latest content: {str(e)}")
    
    return render(request, 'downloader/home.html', {
        'latest_content': latest_content
    })

# Movie Search View
def check_network_connectivity(hostname="api.themoviedb.org", port=443, timeout=5):
    """Check if we can connect to the TMDB API server"""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((hostname, port))
        return True
    except (socket.timeout, socket.error, OSError):
        return False

def make_omdb_request(params):
    """Helper function to make OMDB API requests with proper error handling"""
    try:
        # Add API key to params
        params = params or {}
        params['apikey'] = OMDB_API_KEY
        
        # Make request to OMDB API
        response = requests.get(
            OMDB_BASE_URL,
            params=params,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.json()
        
    except requests.exceptions.Timeout:
        raise Timeout(f"Request to OMDB API timed out after {REQUEST_TIMEOUT} seconds")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            raise ValueError("Invalid OMDB API key. Please check your configuration.")
        elif e.response.status_code == 404:
            raise ValueError("The requested resource was not found on OMDB.")
        else:
            raise
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Failed to connect to OMDB API: {str(e)}")
    except Exception as e:
        raise Exception(f"Error in make_omdb_request: {str(e)}")

def search_movies(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return render(request, 'downloader/movie_search.html')

    try:
        # Search for movies using OMDB API
        params = {
            's': query,
            'type': 'movie',
            'r': 'json'
        }
        
        data = make_omdb_request(params)
        
        if data.get('Response') != 'True':
            return render(request, 'downloader/movie_search.html', 
                        {'error': data.get('Error', 'No results found')})
        
        # Process results
        movies = []
        for movie in data.get('Search', []):
            movies.append({
                'id': movie.get('imdbID', ''),
                'title': movie.get('Title', 'No title available'),
                'year': movie.get('Year', ''),
                'poster_url': movie.get('Poster', ''),
                'type': movie.get('Type', '')
            })
            
        return render(request, 'downloader/movie_search.html', {
            'movies': movies,
            'query': query
        })
        
    except Exception as e:
        return render(request, 'downloader/movie_search.html', {
            'error': f"Error searching for movies: {str(e)}"
        })

# Movie Detail View
def search_youtube_trailer(movie_title, year):
    """Search for movie trailer on YouTube"""
    try:
        search_query = f"{movie_title} {year} official trailer"
        search_url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
        return search_url
    except:
        return None

def movie_detail(request, movie_id):
    try:
        # Get movie details from OMDB API
        params = {
            'i': movie_id,
            'plot': 'full',
            'r': 'json'
        }
        
        movie = make_omdb_request(params)
        
        if movie.get('Response') == 'False':
            raise Exception(movie.get('Error', 'Failed to fetch movie details'))
        
        # Get YouTube trailer URL
        trailer_url = search_youtube_trailer(movie.get('Title', ''), movie.get('Year', ''))
            
        # Format movie data
        movie_data = {
            'id': movie.get('imdbID', ''),
            'title': movie.get('Title', 'No title'),
            'year': movie.get('Year', 'N/A'),
            'rated': movie.get('Rated', 'N/A'),
            'released': movie.get('Released', 'N/A'),
            'runtime': movie.get('Runtime', 'N/A'),
            'genre': movie.get('Genre', 'N/A'),
            'director': movie.get('Director', 'N/A'),
            'writer': movie.get('Writer', 'N/A'),
            'actors': movie.get('Actors', 'N/A'),
            'plot': movie.get('Plot', 'No plot available'),
            'language': movie.get('Language', 'N/A'),
            'country': movie.get('Country', 'N/A'),
            'awards': movie.get('Awards', 'N/A'),
            'poster': movie.get('Poster', ''),
            'ratings': movie.get('Ratings', []),
            'metascore': movie.get('Metascore', 'N/A'),
            'imdb_rating': movie.get('imdbRating', 'N/A'),
            'imdb_votes': movie.get('imdbVotes', 'N/A'),
            'type': movie.get('Type', 'N/A'),
            'dvd': movie.get('DVD', 'N/A'),
            'box_office': movie.get('BoxOffice', 'N/A'),
            'production': movie.get('Production', 'N/A'),
            'website': movie.get('Website', 'N/A'),
            'trailer_url': trailer_url
        }
        
        return render(request, 'downloader/movie_detail.html', {
            'movie': movie_data
        })
        
        if movie.get('Response') != 'True':
            return render(request, 'downloader/error.html', {
                'error': movie.get('Error', 'Movie not found or error fetching details')
            })
        
        # Format movie data
        movie_data = {
            'id': movie.get('imdbID', ''),
            'title': movie.get('Title', 'No title'),
            'year': movie.get('Year', 'N/A'),
            'rated': movie.get('Rated', 'N/A'),
            'released': movie.get('Released', 'N/A'),
            'runtime': movie.get('Runtime', 'N/A'),
            'genre': movie.get('Genre', 'N/A'),
            'director': movie.get('Director', 'N/A'),
            'writer': movie.get('Writer', 'N/A'),
            'actors': movie.get('Actors', 'N/A'),
            'plot': movie.get('Plot', 'No overview available.'),
            'language': movie.get('Language', 'N/A'),
            'country': movie.get('Country', 'N/A'),
            'awards': movie.get('Awards', 'N/A'),
            'poster_url': movie.get('Poster', ''),
            'ratings': movie.get('Ratings', []),
            'metascore': movie.get('Metascore', 'N/A'),
            'imdb_rating': movie.get('imdbRating', 'N/A'),
            'imdb_votes': movie.get('imdbVotes', 'N/A'),
            'type': movie.get('Type', 'N/A'),
            'dvd': movie.get('DVD', 'N/A'),
            'box_office': movie.get('BoxOffice', 'N/A'),
            'production': movie.get('Production', 'N/A'),
            'website': movie.get('Website', 'N/A')
        }
        
        return render(request, 'downloader/movie_detail.html', {
            'movie': movie_data
        })
        
    except Exception as e:
        return render(request, 'downloader/error.html', {
            'error': f"Error fetching movie details: {str(e)}"
        })

import mimetypes
import requests
@csrf_exempt
@require_http_methods(["POST"])
def download_media(request):
    if 'url' not in request.POST:
        return JsonResponse({'status': 'error', 'message': 'URL is required'}, status=400)

    url = request.POST['url'].strip()
    if not url:
        return JsonResponse({'status': 'error', 'message': 'URL cannot be empty'}, status=400)

    media_type = request.POST.get('media_type', 'video')

    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'downloads'), exist_ok=True)
    unique_id = str(uuid.uuid4())

    if media_type == 'image':
        # Download image using requests
        try:
            response = requests.get(url, stream=True)
            if response.status_code != 200:
                return JsonResponse({'status': 'error', 'message': 'Image not found or inaccessible'}, status=400)
            content_type = response.headers.get('content-type')
            ext = mimetypes.guess_extension(content_type) or '.jpg'
            safe_filename = f"{unique_id}{ext}"
            final_path = os.path.join('downloads', safe_filename)
            default_storage.save(final_path, ContentFile(response.content))
            return render(request, 'downloader/download_success.html', {
                'download_url': os.path.join(settings.MEDIA_URL, final_path.replace('\\', '/')),
                'filename': safe_filename
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Error downloading image: {str(e)}'}, status=500)

    # For video/audio, use yt_dlp
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'downloads', unique_id)
    os.makedirs(temp_dir, exist_ok=True)
    # Get quality from form for video
    quality = request.POST.get('quality', 'best') if media_type == 'video' else None
    download_type = request.POST.get('download_type', 'video') if media_type == 'video' else None
    if media_type == 'video' and download_type == 'audio':
        # Download audio as MP3 from video
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'merge_output_format': None,
        }
    else:
        ydl_opts = {
            'format': quality if media_type == 'video' else 'bestaudio/best',
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'merge_output_format': 'mp4' if media_type == 'video' else None,
        }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if not info or 'requested_downloads' not in info or not info['requested_downloads']:
                return JsonResponse({'status': 'error', 'message': 'No downloadable content found'}, status=400)
            downloaded_file = info['requested_downloads'][0]['filepath']
            if not os.path.exists(downloaded_file):
                return JsonResponse({'status': 'error', 'message': 'File not found after download'}, status=500)
            original_filename = os.path.basename(downloaded_file)
            safe_filename = f"{unique_id}_{original_filename}"
            final_path = os.path.join('downloads', safe_filename)
            with open(downloaded_file, 'rb') as f:
                default_storage.save(final_path, ContentFile(f.read()))
            try:
                import shutil
                shutil.rmtree(temp_dir)
            except Exception as e:
                print(f"Error cleaning up temp directory: {e}")
            return render(request, 'downloader/download_success.html', {
                'download_url': os.path.join(settings.MEDIA_URL, final_path.replace('\\', '/')),
                'filename': safe_filename
            })
    except Exception as e:
        if os.path.exists(temp_dir):
            try:
                import shutil
                shutil.rmtree(temp_dir)
            except:
                pass
        error_msg = str(e)
        if 'Unsupported URL' in error_msg:
            return JsonResponse({'status': 'error', 'message': 'Unsupported URL or service'}, status=400)
        elif 'Video unavailable' in error_msg:
            return JsonResponse({'status': 'error', 'message': 'Video is unavailable or private'}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': f'Error downloading media: {error_msg}'}, status=500)

def download_movie(request, movie_id):
    """
    View to handle movie downloads from TMDB
    """
    try:
        # Get movie details from TMDB
        movie_url = f"{TMDB_BASE_URL}/movie/{movie_id}"
        params = {
            'api_key': TMDB_API_KEY,
            'language': 'hi',
            'append_to_response': 'videos,release_dates'
        }
        
        response = requests.get(movie_url, params=params)
        if response.status_code != 200:
            return render(request, 'downloader/error.html', {
                'message': 'Failed to fetch movie details from TMDB.'
            })
        
        movie = response.json()
        movie_title = movie.get('title', 'movie').replace(' ', '_')
        
        # Try to find a YouTube trailer
        video_url = None
        if 'videos' in movie and 'results' in movie['videos']:
            for video in movie['videos']['results']:
                if video['site'] == 'YouTube' and video['type'] == 'Trailer':
                    video_url = f"https://www.youtube.com/watch?v={video['key']}"
                    break
        
        if not video_url:
            return render(request, 'downloader/error.html', {
                'message': 'No downloadable content found for this movie.'
            })
        
        # Prepare download directory
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'downloads'), exist_ok=True)
        unique_id = str(uuid.uuid4())
        output_dir = os.path.join(settings.MEDIA_ROOT, 'downloads', unique_id)
        os.makedirs(output_dir, exist_ok=True)
        
        # Download options
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(output_dir, f'{movie_title}.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'merge_output_format': 'mp4',
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['hi', 'en'],
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }
        
        # Start download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            if not info or 'requested_downloads' not in info or not info['requested_downloads']:
                return render(request, 'downloader/error.html', {
                    'message': 'Failed to download the video.'
                })
            
            downloaded_file = info['requested_downloads'][0]['filepath']
            if not os.path.exists(downloaded_file):
                return render(request, 'downloader/error.html', {
                    'message': 'File not found after download.'
                })
            
            # Move file to final location
            filename = f"{movie_id}_{os.path.basename(downloaded_file)}"
            final_path = os.path.join('downloads', filename)
            with open(downloaded_file, 'rb') as f:
                default_storage.save(final_path, ContentFile(f.read()))
            
            # Cleanup
            try:
                import shutil
                shutil.rmtree(output_dir)
            except Exception as e:
                print(f"Error cleaning up directory: {e}")
            
            # Get file size
            file_size = os.path.getsize(os.path.join(settings.MEDIA_ROOT, final_path))
            
            return render(request, 'downloader/download_success.html', {
                'download_url': os.path.join(settings.MEDIA_URL, final_path.replace('\\', '/')),
                'filename': filename,
                'movie_title': movie.get('title', 'Movie'),
                'file_size': file_size
            })
    
    except Exception as e:
        return render(request, 'downloader/error.html', {
            'message': f'An error occurred: {str(e)}'
        })

def weather_dashboard(request):
    return render(request, 'downloader/weather_dashboard.html')
