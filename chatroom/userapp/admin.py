from django.contrib import admin
from .models import *

# Register your models here.
class UserManager(admin.ModelAdmin):
    list_display = ['id', 'username', 'telnumber','created_time','is_active']  # 列表显示
    list_display_links = ['username','telnumber']  # 点击跳转的位置
    search_fields = ['username', 'id']  # 搜索框,参数是搜索的列
    ordering = ('id',)

admin.site.register(User,UserManager)
