# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-25 10:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20180625_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bt_test',
            name='av_name',
            field=models.CharField(max_length=200),
        ),
    ]
