from django.db import models

class Parser(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    script = models.FileField(upload_to=".parsers")
    scheduled = models.DateTimeField(null=True, blank=True)
    repeat_after = models.DurationField(null=True, blank=True)
