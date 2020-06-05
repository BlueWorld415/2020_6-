# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-04-22 12:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('room', '0012_auto_20200419_2010'),
        ('userapp', '0006_auto_20200404_1541'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='公告内容')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('room', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='room.Room_list', verbose_name='聊天室')),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='userapp.User', verbose_name='发布者')),
            ],
            options={
                'db_table': 'notices',
            },
        ),
    ]
