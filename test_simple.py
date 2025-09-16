import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studyshala.settings')
django.setup()

# Now we can import our models
from farm.models import WeatherAlert

def main():
    # Test database connection
    try:
        count = WeatherAlert.objects.count()
        print(f"Connected to database. Found {count} weather alerts.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
