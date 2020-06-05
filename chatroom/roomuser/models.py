from django.db import models

# Create your models here.
from room.models import Room_list
from userapp.models import User


class RoomUser(models.Model):
    room=models.ForeignKey(Room_list)
    user=models.ForeignKey(User)
    join_time=models.DateTimeField(auto_now_add=True,verbose_name='进入时间')
    is_active=models.SmallIntegerField(verbose_name='是否可用',choices=((0,'不可进入'),(1,'可进入')),default=1)
    class Meta:
        db_table='roomuser'
        verbose_name='聊天室成员'
        verbose_name_plural='聊天室成员列表'