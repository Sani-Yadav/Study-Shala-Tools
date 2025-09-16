from django.apps import AppConfig


class IdCardAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "political_id.id_card_app"
    label = "id_card_app"
    verbose_name = "Political ID"
