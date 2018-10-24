# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-24 10:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_profile_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={},
        ),
        migrations.AddField(
            model_name='booking',
            name='is_scheduled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='booking',
            name='slot_date',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='slot_end_time',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='slot_time',
            field=models.CharField(max_length=20, null=True),
        ),
    ]