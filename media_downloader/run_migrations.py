import os
import sys

def run_migrations():
    # Set the default environment variable for Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'media_downloader.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    
    # Create migrations
    print("\nCreating migrations...")
    execute_from_command_line(['manage.py', 'makemigrations', 'downloader'])
    
    # Apply migrations
    print("\nApplying migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("\nMigrations completed successfully!")

if __name__ == "__main__":
    run_migrations()
