# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-05-01 02:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notice',
            options={'verbose_name': '公告', 'verbose_name_plural': '公告列表'},
        ),
    ]
