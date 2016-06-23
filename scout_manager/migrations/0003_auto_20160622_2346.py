# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-22 23:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scout_manager', '0002_auto_20160617_0005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='group_id',
            field=models.CharField(max_length=500, unique=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='netid',
            field=models.CharField(max_length=40, unique=True),
        ),
    ]