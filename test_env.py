import sys
import os
import platform

def print_section(title):
    print("\n" + "="*50)
    print(f"{title}".center(50))
    print("="*50)

# Print system information
print_section("System Information")
print(f"Platform: {platform.platform()}")
print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version}")
print(f"Current Working Directory: {os.getcwd()}")

# Check Django installation
try:
    import django
    print_section("Django Information")
    print(f"Django Version: {django.__version__}")
    
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studyshala.settings')
    django.setup()
    
    # Check installed apps
    from django.conf import settings
    print_section("Django Settings")
    print(f"Installed Apps: {settings.INSTALLED_APPS}")
    
    # Check if media_downloader is in installed apps
    print("\nChecking media_downloader in installed apps:")
    print('media_downloader.downloader' in settings.INSTALLED_APPS)
    
    # Try to import media_downloader
    try:
        print_section("Testing media_downloader Import")
        import media_downloader
        print(f"Successfully imported media_downloader from: {media_downloader.__file__}")
        
        try:
            from media_downloader.downloader import test_view
            print(f"Successfully imported test_view: {test_view.test_view}")
        except ImportError as e:
            print(f"Failed to import test_view: {e}")
            
    except ImportError as e:
        print(f"Failed to import media_downloader: {e}")
        
    # Check URLs
    try:
        print_section("URL Configuration")
        from django.urls import get_resolver
        urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])
        print(f"Root URLConf: {settings.ROOT_URLCONF}")
        
        # Print all URL patterns
        print("\nURL Patterns:")
        for pattern in urlconf.urlpatterns:
            print(f"- {pattern.pattern}")
            
    except Exception as e:
        print(f"Error checking URL configuration: {e}")
    
except ImportError as e:
    print_section("Error")
    print(f"Django is not properly installed: {e}")
    print("Please make sure Django is installed in your Python environment.")
    print("You can install it using: pip install django")

# Print Python path
print_section("Python Path")
for i, path in enumerate(sys.path, 1):
    print(f"{i}. {path}")

# Check if media_downloader directory exists
print_section("Directory Check")
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
media_downloader_path = os.path.join(project_root, 'media_downloader')
print(f"Checking if media_downloader exists at: {media_downloader_path}")

if os.path.exists(media_downloader_path):
    print("media_downloader directory exists!")
    print("Contents of media_downloader directory:")
    for item in os.listdir(media_downloader_path):
        item_path = os.path.join(media_downloader_path, item)
        print(f"- {item} ({'dir' if os.path.isdir(item_path) else 'file'})")
        
        # Check for __init__.py in subdirectories
        if os.path.isdir(item_path) and '__init__.py' in os.listdir(item_path):
            print(f"  - Contains __init__.py")
else:
    print("media_downloader directory does not exist at the expected location!")
