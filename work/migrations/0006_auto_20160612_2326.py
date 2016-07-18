# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-12 23:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0005_auto_20160610_0123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientaddress',
            name='city',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='clientaddress',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='work.Client'),
        ),
        migrations.AlterField(
            model_name='clientaddress',
            name='state',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='clientaddress',
            name='street',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='clientaddress',
            name='zip_code',
            field=models.TextField(null=True),
        ),
    ]
