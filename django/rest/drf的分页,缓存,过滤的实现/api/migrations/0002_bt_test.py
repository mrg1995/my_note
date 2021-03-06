# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-23 12:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bt_test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('av_name', models.CharField(max_length=200)),
                ('magent', models.CharField(max_length=200)),
                ('hash_info', models.CharField(max_length=100)),
                ('time_info', models.DateTimeField(help_text='创建时间')),
                ('size_info', models.CharField(help_text='大小', max_length=50)),
                ('user', models.ManyToManyField(help_text='浏览过该种子的用户', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'bts',
                'ordering': ['-id'],
            },
        ),
    ]
