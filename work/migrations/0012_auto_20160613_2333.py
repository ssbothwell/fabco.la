# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-13 23:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0011_lineitem_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lineitem',
            name='total_price',
        ),
        migrations.RemoveField(
            model_name='project',
            name='cost_total',
        ),
    ]