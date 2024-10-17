from django.db import models
from django.db.models.signals import post_save


class Parser(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    script = models.FileField(upload_to=".parsers")
    scheduled = models.DateTimeField(null=True, blank=True)
    repeat_after = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"Parser({self.id}, {self.name})"

    @property
    def job_id(self):
        return str(self.id)

    @staticmethod
    def post_save(sender, instance, created, **kwargs):
        from .schedule import schedule
        from .scheduler import scheduler

        schedule(scheduler, instance)


post_save.connect(Parser.post_save, sender=Parser)
