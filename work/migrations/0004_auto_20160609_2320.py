# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-09 23:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0003_auto_20160609_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='completion_date',
            field=models.DateField(blank=True, null=True, verbose_name='date completed'),
        ),
        migrations.AlterField(
            model_name='project',
            name='confirmation_date',
            field=models.DateField(blank=True, null=True, verbose_name='confirmation date'),
        ),
        migrations.AlterField(
            model_name='project',
            name='due_date',
            field=models.DateField(blank=True, null=True, verbose_name='due date'),
        ),
    ]