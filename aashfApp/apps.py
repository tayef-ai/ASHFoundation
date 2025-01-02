from django.apps import AppConfig


class AashfappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aashfApp'
    verbose_name = 'ASH Foundation'
    def ready(self):
        import aashfApp.signals

