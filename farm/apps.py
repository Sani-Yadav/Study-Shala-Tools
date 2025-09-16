from django.apps import AppConfig


class FarmConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "farm"
    verbose_name = "किसान सहायक"  # Hindi name for better admin interface
