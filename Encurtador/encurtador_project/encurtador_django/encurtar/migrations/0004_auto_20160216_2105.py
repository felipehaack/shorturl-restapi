# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-16 21:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encurtar', '0003_auto_20160216_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
