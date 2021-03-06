# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-04-19 09:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('room', '0011_remove_room_list_user'),
        ('userapp', '0006_auto_20200404_1541'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('join_time', models.DateTimeField(auto_created=True, verbose_name='进入时间')),
                ('is_active', models.SmallIntegerField(choices=[(0, '不可进入'), (1, '可进入')], default=1, verbose_name='是否可用')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room.Room_list')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userapp.User')),
            ],
            options={
                'verbose_name': '聊天室成员',
                'verbose_name_plural': '聊天室成员列表',
                'db_table': 'roomuser',
            },
        ),
    ]
