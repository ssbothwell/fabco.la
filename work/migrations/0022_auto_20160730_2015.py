# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-30 20:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0021_auto_20160704_0305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='discount',
            field=models.IntegerField(default=0),
        ),
    ]
