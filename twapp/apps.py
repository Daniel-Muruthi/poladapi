from django.apps import AppConfig


class TwappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'twapp'

    def ready(self):
        from twapp import signals
        from twapp import automation
        from twapp import tweet_handlers
        from twapp import scheduler
        # scheduler.start()


    



