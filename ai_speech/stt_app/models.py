from django.db import models

class voice(models.Model):
    name = models.TextField(max_length=144, blank=False)
    file = models.FileField(upload_to="audio/")
