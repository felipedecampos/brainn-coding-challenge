from django.db import models


# Create your models here.
class Repository(models.Model):
    repository_id = models.CharField(max_length=511)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=511)
    languages = models.CharField(max_length=511)
    tags = models.CharField(max_length=1023)
