from django.db import models


# Create your models here.
class Store(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=800)
    rating = models.IntegerField()
