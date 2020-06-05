from django.db import models
# Create your models here.
class User(models.Model):
    username=models.CharField('用户名',max_length=20,unique=True)
    password=models.CharField('密码',max_length=32)
    telnumber=models.CharField('手机号码',max_length=11)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)
    is_active = models.BooleanField('是否活跃',default=True)

    def __str__(self):
        return self.username
    class Meta:
        db_table='user'
        verbose_name='用户'
        verbose_name_plural=verbose_name

