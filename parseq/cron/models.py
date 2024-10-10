from django.db import models
from .tasks import send_run_actor
from django.db.models.signals import post_save
from apscheduler.jobstores.base import JobLookupError

class Parser(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    script = models.FileField(upload_to=".parsers")
    scheduled = models.DateTimeField(null=True, blank=True)
    repeat_after = models.DurationField(null=True, blank=True)

    @staticmethod
    def post_save(sender, instance, created, **kwargs):
        from .scheduler import scheduler

        job_id = str(instance.id)
        args = (instance.name,instance.script.path)

        try:
            scheduler.remove_job(job_id)
        except JobLookupError:
            pass

        if instance.scheduled is not None:
            if instance.repeat_after is None:
                scheduler.add_job(send_run_actor, 'date', args = args, run_date=instance.scheduled, id=job_id)
            else:
                scheduler.add_job(send_run_actor, 'interval', args = args, seconds=instance.repeat_after.seconds, start_date=instance.scheduled, id=job_id)

post_save.connect(Parser.post_save, sender=Parser)