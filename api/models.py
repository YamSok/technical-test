from django.db import models

class MountainPeak(models.Model):
    name = models.CharField(max_length=255)
    lat = models.FloatField()
    lon = models.FloatField()
    altitude = models.FloatField()
