import sys
from django.apps import AppConfig

class CronConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cron'

    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        
        from .models import Parser
        from .schedule import schedule
        from .scheduler import scheduler
        
        for parser in Parser.objects.all():
            schedule(scheduler, parser)
            
        scheduler.start()
