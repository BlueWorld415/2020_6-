from django.contrib import admin
from .models import RoomUser
from userapp.models import User
# Register your models here.
class RoomUserManager(admin.ModelAdmin):
    list_display = ['id', 'room', 'user','join_time','is_active']
    list_display_links = ['id','room','user','join_time']
    search_fields = ['user','room', 'id']
    ordering = ('id',)
    list_editable = [ 'is_active']
    def user(self,obj):
        return obj.user.username
    def room(self,obj):
        return obj.room.roomname


admin.site.register(RoomUser, RoomUserManager)