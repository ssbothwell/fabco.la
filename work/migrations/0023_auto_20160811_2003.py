# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-11 20:03
from __future__ import unicode_literals

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0022_auto_20160730_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='lineitem',
            name='description',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]