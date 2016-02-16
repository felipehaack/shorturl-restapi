from __future__ import unicode_literals

from django.db import models

class User(models.Model):
	name = models.CharField(max_length=50, unique=True)

class Url(models.Model):
    url = models.URLField(max_length=500, default='')
    shorturl = models.URLField(max_length=500, default='')
    hint = models.IntegerField()
    user = models.ForeignKey(User)