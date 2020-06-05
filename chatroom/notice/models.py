from django.db import models

# Create your models here.
from room.models import Room_list
from userapp.models import User


class Notice(models.Model):
    room=models.ForeignKey(Room_list,verbose_name='聊天室',default=0)
    user=models.ForeignKey(User,verbose_name='发布者',default=0)
    content=models.TextField('公告内容')
    created_time = models.DateTimeField('发布时间', auto_now_add=True)
    class Meta:
        db_table='notices'
        verbose_name='公告'
        verbose_name_plural='公告列表'
