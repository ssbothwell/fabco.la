# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-10 01:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0004_auto_20160609_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='deposit',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
