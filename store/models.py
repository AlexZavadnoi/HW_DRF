from django.db import models


class Store(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    description = models.CharField(max_length=800, verbose_name='Description')
    rating = models.IntegerField()
    owner = models.ForeignKey(
        'auth.User',
        verbose_name='Owner',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    status = models.CharField(
        default='',
        max_length=20,
        choices=(('in_review', 'In Review'), ('active', 'Active'), ('deactivated', 'Deactivated')))
