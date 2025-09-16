import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studyshala.settings')
django.setup()

from django.apps import apps

# List all installed apps
print("\nInstalled apps:")
for app_config in apps.get_app_configs():
    print(f"- {app_config.name}")

# Check if our app is registered
try:
    app_config = apps.get_app_config('id_card_app')
    print(f"\nApp found: {app_config.name}")
    print(f"Models in this app: {[m.__name__ for m in app_config.get_models()]}")
except LookupError:
    print("\nApp 'id_card_app' not found in app registry")
