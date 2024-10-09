from django.db import models

class Parser(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    script = models.FileField()
    scheduled = models.DateTimeField(null=True)
    repeat_after = models.DurationField(null=True)
