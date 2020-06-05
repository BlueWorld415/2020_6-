from django.contrib import admin
from .models import Notice
# Register your models here.
class NoticeManager(admin.ModelAdmin):
    list_display = ['id', 'content', 'room_id', 'user_id','created_time']
    list_display_links=['id','content']
    search_fields = ['content', 'id']


admin.site.register(Notice, NoticeManager)