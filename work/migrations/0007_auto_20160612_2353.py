# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-12 23:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0006_auto_20160612_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientaddress',
            name='client',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='work.Client'),
        ),
    ]
