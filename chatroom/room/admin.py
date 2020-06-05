from django.contrib import admin
from .models import *

# Register your models here.

class RoomManager(admin.ModelAdmin):
    list_display = ['id','roomname','owner','created_time']# 列表显示
    list_display_links = ['roomname']# 点击跳转的位置
    search_fields = ['roomname','id']#搜索框,参数是搜索的列

class FileManager(admin.ModelAdmin):
    list_display=['id','fname','fpath','room_id','user_id','upload_time']
    list_display_links=['fname','fpath']
    search_fields=['fname','id']
class RecordManager(admin.ModelAdmin):
    list_display=['content','sent_time','room_id','user_id']
    
    search_fields=['fname','id']
admin.site.register(Room_list, RoomManager)
admin.site.register(Files, FileManager)
# admin.site.register(Record, RecordManager)