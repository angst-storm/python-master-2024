from django.db import models
from .tasks import send_run_actor
from django.db.models.signals import post_save
from apscheduler.jobstores.base import JobLookupError, ConflictingIdError
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger

class Parser(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    script = models.FileField(upload_to=".parsers")
    scheduled = models.DateTimeField(null=True, blank=True)
    repeat_after = models.DurationField(null=True, blank=True)

    @property
    def job_id(self):
        return str(self.id)

    @staticmethod
    def post_save(sender, instance, created, **kwargs):
        from .scheduler import scheduler

        job_id = instance.job_id

        try:
            scheduler.pause_job(job_id)
        except JobLookupError:
            pass

        if instance.scheduled is not None:
            try:
                scheduler.add_job(id=job_id, func=send_run_actor, args = (instance.id,instance.name,instance.script.path))
            except ConflictingIdError:
                pass

            if instance.repeat_after is None:
                scheduler.reschedule_job(job_id, trigger=DateTrigger(instance.scheduled))
            else:
                scheduler.reschedule_job(job_id, trigger=IntervalTrigger(seconds=instance.repeat_after.seconds, start_date=instance.scheduled))

            scheduler.resume_job(job_id)

post_save.connect(Parser.post_save, sender=Parser)