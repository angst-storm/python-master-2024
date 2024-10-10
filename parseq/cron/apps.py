from django.apps import AppConfig

class CronConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cron'

    def ready(self):
        from .scheduler import scheduler
        
        scheduler.start()
