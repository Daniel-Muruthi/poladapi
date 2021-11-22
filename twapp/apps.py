from django.apps import AppConfig


class TwappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'twapp'

    def ready(self):
        import twapp.automation


    



