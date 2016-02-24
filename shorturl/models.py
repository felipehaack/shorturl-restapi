from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class User(models.Model):

    name = models.CharField(max_length=50, default='', unique=True)

    def __str__(self):
        return self.name

class Url(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="urls")
    url = models.URLField(max_length=200, default='', unique=True)
    shortUrl = models.URLField(max_length=100, default='', unique=True)
    hits = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return self.url