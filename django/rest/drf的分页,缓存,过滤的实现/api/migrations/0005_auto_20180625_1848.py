# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-25 10:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20180624_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bt_test',
            name='av_name',
            field=models.CharField(db_index=True, max_length=200),
        ),
    ]
