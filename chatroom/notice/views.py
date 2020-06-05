import json

from django.http import JsonResponse
from django.shortcuts import render
import redis
# Create your views here.
from notice.models import Notice

r=redis.Redis('127.0.0.1',6379,db=4)

def send(request):
    request_json=json.loads(request.body)
    content=request_json.get('content')
    rid=request.session.get('rid')
    uid=request.session.get('uid')
    try:
        n=Notice.objects.create(content=content,user_id=uid,room_id=rid)
    except Exception as e:
        print('公告消息入库失败',e)
    # print(request_json.get('content'))
    return JsonResponse({'code':200,'msg':'发布成功'})


def get(request):
    rid=request.session.get('rid')
    notices=Notice.objects.filter(room_id=rid).order_by('-created_time')
    data=[]
    for notice in notices:
        n={}
        n['content']=notice.content
        n['created_time']=notice.created_time.strftime('%Y-%m-%d %H:%M:%S')
        data.append(n)
    return JsonResponse({'code':200,'data':data})


def new(request):
    rid = request.session.get('rid')
    uid = request.session.get('uid')
    notices = Notice.objects.filter(room_id=rid).order_by('-id')
    new_id= notices[0].id if notices else 0
    if not r.exists(f"user{uid}_room{rid}_notice"):
        r.set(f"user{uid}_room{rid}_notice", new_id)
    old_redis_notice_id = int(r.get(f"user{uid}_room{rid}_notice").decode())
    notices = Notice.objects.filter(room_id=rid).order_by('-id')
    print(old_redis_notice_id, 'noticeredisid')
    # print(notices[0].id, 'noticeistid')
    if notices:
        if old_redis_notice_id == notices[0].id:
            data = []
        else:
            data = []
            for notice in notices:
                if notice.id > old_redis_notice_id:
                    item = {}
                    item['content'] = notice.content
                    item['created_time'] = notice.created_time.strftime('%Y-%m-%d %H:%M:%S')
                    data.append(item)
        new_id= notices[0].id if notices else 0
        r.set(f"user{uid}_room{rid}_notice", new_id)
    else:
        data=[]
    return JsonResponse({'code': 200, 'data': data ,'msg':'新的公告'})