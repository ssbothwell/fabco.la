# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-18 23:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0017_auto_20160616_0758'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='discount',
            field=models.FloatField(null=True),
        ),
    ]
