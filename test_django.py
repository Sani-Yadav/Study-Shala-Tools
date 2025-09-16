import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studyshala.settings')
django.setup()

# Now we can import Django models and other modules
from django.conf import settings

print("Installed apps:")
for app in settings.INSTALLED_APPS:
    print(f"- {app}")

print("\nChecking if media_downloader.downloader is in installed apps:")
print('media_downloader.downloader' in settings.INSTALLED_APPS)

try:
    from django.urls import get_resolver
    print("\nURL patterns for media-downloader/:")
    resolver = get_resolver()
    try:
        url_patterns = [pattern.pattern._route for pattern in resolver.url_patterns if 'media-downloader' in str(pattern.pattern)]
        print("Found URL patterns:", url_patterns)
    except Exception as e:
        print(f"Error getting URL patterns: {e}")
    
    print("\nTrying to import media_downloader.downloader.views...")
    from media_downloader.downloader import views
    print("Successfully imported views:", dir(views))
    
    print("\nTrying to import test_view...")
    from media_downloader.downloader import test_view
    print("Successfully imported test_view:", dir(test_view))
    
except Exception as e:
    print(f"Error: {e}")
    print("\nCurrent Python path:")
    import sys
    for path in sys.path:
        print(f"- {path}")
