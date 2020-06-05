import json

from django.http import JsonResponse
from django.shortcuts import render
import redis

# Create your views here.
from room.models import Room_list
from roomuser.models import RoomUser
from userapp.models import User

r=redis.Redis('127.0.0.1',6379,db=5)

def setView(request):
    rid = request.session.get('rid')
    uid = request.session.get('uid')
    try:
        user=RoomUser.objects.get(room_id=rid,user_id=uid)
        if not user.is_active:
            return JsonResponse({'code':404,'data':'sent out'})

    except:
        RoomUser.objects.create(room_id=rid,user_id=uid)
    print('创建成功')
    oid = request.session.get('oid')
    o_on = 1 if oid == uid else 0
    return JsonResponse({'code': 200, 'data': 'set success'})


def getView(request):
    rid = request.session.get('rid')
    uid=request.session.get('uid')
    if not r.exists(f"user{uid}_room{rid}_users"):
        r.set(f"user{uid}_room{rid}_users",0)
    old_redis_id=int(r.get(f"user{uid}_room{rid}_users").decode())
    data=RoomUser.objects.filter(room_id=rid,is_active=1).order_by('-id')
    l=[]    
    if data[0].id==old_redis_id:
        return JsonResponse({'code': 200, 'data': l})
    elif not old_redis_id==0:
        for users in data:
            if users.id>old_redis_id:
                item={}
                item['id']=users.user.id
                item['username']=users.user.username
                l.append(item)
    else:
        for users in data :
            item={}
            item['id']=users.user.id
            item['username']=users.user.username
            l.append(item)
    r.set(f"user{uid}_room{rid}_users", data[0].id)

    return JsonResponse({'code': 200, 'data': l})



def outView(request):
    # print('000000000000000000000',request.GET.get('name'))
    outname=request.GET.get('name')
    outrid=request.session.get('rid')
    outuid=User.objects.get(username=outname).id
    print(f'outuid is {outuid},outrid is {outrid}')
    item = RoomUser.objects.get(user_id=outuid,room_id=outrid)
    item.is_active=0
    item.save()
    return JsonResponse({'code':200,'data':'out success'})


def transferView(request):
    rjson=json.loads(request.body)
    tname=rjson.get('tname')
    rid=request.session.get('rid')
    new_owner=User.objects.get(username=tname)
    room=Room_list.objects.get(id=rid)
    room.owner=new_owner.id
    room.save()

    return JsonResponse({'code':200,'msg':'已转让给'+tname})