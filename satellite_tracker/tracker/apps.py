from django.apps import AppConfig


class TrackerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "satellite_tracker.tracker"
    verbose_name = "Satellite Tracker"
