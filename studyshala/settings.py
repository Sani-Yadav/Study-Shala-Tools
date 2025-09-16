from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-secret-key'
DEBUG = True
ALLOWED_HOSTS = []

# TMDB API Configuration
TMDB_API_KEY = "3d1cb94d909aab088231f5af899dffdc"
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_IMAGE_BASE = 'https://image.tmdb.org/t/p/w500'

INSTALLED_APPS = [
    # Django built-in apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken',
    'widget_tweaks',
    
    # Local apps with custom AppConfig
    'employeeid.apps.EmployeeidConfig',
    'qr_feedback.feedback',  # Updated to use the correct app path
    'health_assist.apps.HealthAssistConfig',
    'idcard.apps.IdcardConfig',
    'qr_attendance.attendance.apps.AttendanceConfig',
    'resume.apps.ResumeConfig',
    'scanner.apps.ScannerConfig',
    
    # Local apps without custom AppConfig
    'accounts',
    'notes',
    'media_downloader.downloader',
    
    # Satellite Tracker app with full path
    'satellite_tracker.tracker.apps.TrackerConfig',
    
    # Farm app (ONLY farm, remove farmer_assistant.farm)
    'farm.apps.FarmConfig',
    'social_post',
    'sarkarisahyogi.jobform.apps.JobformConfig',
    'political_id.id_card_app.apps.IdCardAppConfig',  # Using full path to AppConfig
    'ticket_booking.booking.apps.BookingConfig',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'studyshala.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # global template folder
            os.path.join(BASE_DIR, 'accounts', 'templates'),  # accounts app templates
            os.path.join(BASE_DIR, 'sarkarisahyogi', 'templates'),  # sarkarisahyogi app templates
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'studyshala.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.CustomUser'

# OpenWeatherMap API Configuration
OPENWEATHER_API_KEY = 'eb5c7e956d137db93d3ce624f523ce37'  # यहां सिर्फ API key लिखें
