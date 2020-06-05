import json
import shutil
import simplejson
import redis
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from roomuser.views import *
from roomuser.models import RoomUser
from .models import *
from userapp.models import User
from django.conf import settings
import os

rd=redis.Redis('127.0.0.1',6379,db=5)

# Create your views here.
def check_login(request):
    if request.session.get('username'):
        return True
    else:
        return False


def check_file(fname, dir):
    if fname in os.listdir(dir):
        print('文件',fname)
        print('文件列表',os.listdir(dir))
        print('dizhi',dir)
        point = fname.find('.')
        fname = fname[:point] + '(2)' + fname[point:]

        return check_file(fname,dir)
    else:
        return fname

def index(request):
    return render(request, 'index.html')


def room(request):
    if request.method == "GET":
        print(request.session.get('username'))
        # 判断是否已登录
        if check_login(request):
            # 获取聊天室列表
            room_list = Room_list.objects.values('id', 'roomname', 'owner', 'introduce')
            # queryset转json
            data=[]
            for room in room_list:
               res={}
               res['id']=room['id']
               res['roomname']=room['roomname']
               res['owner']=User.objects.get(id=room['owner']).username
               res['introduce']=room['introduce']
               data.append(res)
            
            # room_list = json.dumps(list(map(dict, room_list)))
            print(room_list)
            if room_list:
                return HttpResponse(
                    json.dumps({'code': '20', "data": data, 'user': request.session.get('username')}))
            else:
                return HttpResponse(json.dumps({'code': '41', 'data': '暂时没有聊天室'}))
        else:
            return HttpResponse(json.dumps({'code': '40', 'data': {"msg": "没有登录"}, }))

    elif request.method == "POST":
        # 新建聊天室
        # 获取数据
        request_json = simplejson.loads(request.body.decode())
        r_name = request_json.get("r_name")
        r_intro = request_json.get('r_intro')
        username = request.session.get('username')
        # print(owner,'创建',r_name,'简介',r_intro)
        # 检查数据
        if Room_list.objects.filter(roomname=r_name):
            return HttpResponse(json.dumps({'code': '43', 'msg': '聊天室名称重复'}))
        # 录入数据库
        owner = User.objects.get(username=username)
        try:
            room = Room_list.objects.create(roomname=r_name, introduce=r_intro, owner=owner)
        except Exception as e:
            print('新聊天室入库错误', e)
            return HttpResponse(json.dumps({'code': '42', 'msg': '聊天室入库错误'}))
        os.mkdir(os.path.join(settings.MEDIA_ROOT, f'{room.id}/'))
        return HttpResponse(json.dumps({"code": '21', 'msg': '创建成功'}))


def chat(request):
    if not check_login(request):
        return HttpResponseRedirect('/user/login')

    if request.method == 'GET':
        leave(request)
        print(request.GET)
        roomname = request.GET.get('rname')
        uid=request.session.get('uid')
        # RoomUser.
        # 获取rid
        r = Room_list.objects.filter(roomname=roomname)
        if r:
            rid = r[0].id
            oid = r[0].owner_id
            oname = User.objects.get(id=oid).username
        else:
            # 没有找到这个聊天室
            return HttpResponse('没有找到聊天室,不要自己拼连接哟')
        request.session['roomname'] = roomname
        request.session['rid'] = rid
        request.session['ownername'] = oname
        request.session['oid']=oid
        owner_online='true' if uid==oid else 'false'
        return render(request, 'room.html', {'roomname': roomname, 'owner_online':owner_online,'username': request.session.get('username')})
    elif request.method == 'POST':
        # 判断请求
        request_json = simplejson.loads(request.body.decode())
        if request_json.get('msg') == 'say':
            # 获取数据
            mes = request_json.get('message')
            uid = request.session.get('uid')
            rid = request.session.get('rid')
            print(uid, rid, mes)
            try:
                # 将聊天记录写入数据库
                Record.objects.create(user_id=uid, room_id=rid, content=mes)
            except Exception as e:
                print('发送消息出错', e)
                return json.dumps({'code': '40', 'msg': "发送失败"})
            return HttpResponse(json.dumps({'code': '11', 'msg': "发送成功"}))
        elif request_json.get('msg') == 'read':
            r_name = request.session['roomname']
            oname = request.session['ownername']
            uid=request.session['uid']
            rid=request.session['rid']
            print('room-name----------', r_name)
            if not rd.exists(f"user{uid}_room{rid}_record"):
                rd.set(f"user{uid}_room{rid}_record", 0)
            old_redis_record_id = int(rd.get(f"user{uid}_room{rid}_record").decode())
            records = Record.objects.filter(room__roomname=r_name).values('id','user__username', 'content', 'sent_time').order_by('-id')
            print(old_redis_record_id,'redisid')
            # print(records[0]['id'],'recordid')
            if records:
                if old_redis_record_id==records[0]['id']:
                    data=[]
                    return JsonResponse({'code': '20', 'data': data, 'user': request.session['username'], 'owner': oname})
                elif not old_redis_record_id==0:
                    records=[record for record in records if record['id']>old_redis_record_id]
                data = []
                for record in reversed(records):
                    item={}
                    item['id']=record['id']
                    item['user__username']=record['user__username']
                    item['content']=record['content']
                    item['sent_time']=record['sent_time'].strftime('%Y-%m-%d %H:%M:%S')
                    data.append(item)
                print(records)
                new_id=records[0]['id'] if records else 0
                rd.set(f"user{uid}_room{rid}_record", new_id)
            else:
                data=[]
            return JsonResponse({'code': '20', 'data': data, 'user': request.session['username'], 'owner': oname})
        else:
            return HttpResponse(json.dumps({'code': '41', 'msg': '无法识别ajax代码'}))


def upload(request):
    if request.method == 'POST':
        fl = request.FILES['file']
        rid = request.session['rid']
        print('上传的文件名', fl.name)
        fname = fl.name
        fname=check_file(fname,settings.MEDIA_ROOT+ f'/{rid}')
        print('检查',fname)
        filename=os.path.join(settings.MEDIA_ROOT,f'{rid}/'+fname)

        print('文件',filename)
        with open(filename, 'wb') as f:
            f.write(fl.file.read())
        Files.objects.create(fname=fname, fpath=filename, user_id=request.session.get('uid'),
                             room_id=request.session.get('rid'))

        return JsonResponse({'code':200,'msg':'上传成功'})


def files(request):
    rid = request.session.get('rid')
    uid=request.session.get('uid')
    if not rd.exists(f"user{uid}_room{rid}_files"):
        rd.set(f"user{uid}_room{rid}_files",0)
    old_redis_files_id=int(rd.get(f"user{uid}_room{rid}_files").decode())
    file_list = Files.objects.filter(room_id=rid).values('id','fname', 'upload_time').order_by('-id')
    print(old_redis_files_id,'redisid')
    print(file_list[0]['id'],'filelistid')
    path=f'/static/files/{rid}/'

    if old_redis_files_id==file_list[0]['id']:
        data=[]
        return JsonResponse({'code': 200, 'data': data, 'path': path})
    elif not old_redis_files_id == 0:
        file_list = [file for file in file_list if file['id'] > old_redis_files_id]
    data = []
    for file in reversed(file_list):
        item={}
        item['id']=file['id']
        item['fname']=file['fname']
        item['upload_time']=file['upload_time'].strftime('%Y-%m-%d %H:%M:%S')
        data.append(item)
        rd.set(f"user{uid}_room{rid}_files", file_list[0]['id'])

    return JsonResponse({'code':200,'data':data,'path':path})


def dissolution(request):
    rid = request.session['rid']
    if request.session['ownername'] == request.session['username']:
        try:
            room = Room_list.objects.get(id=rid)
            room.delete()
            print(os.path.join(settings.MEDIA_ROOT, f'{rid}/'))
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, f'{rid}/'))
        except Exception as e:
            print('解散聊天室时出错', e)
            return HttpResponse(json.dumps({'code': '40', 'msg': '解散失败'}))
    del request.session['roomname']
    del request.session['rid']
    return HttpResponse(json.dumps({'code': '21', 'msg': '退出成功'}))


def remove(request):
    rid=request.session['rid']
    file_id=request.GET.get('file_id')
    fid=file_id.split('_')[-1]
    print(fid)
    file=Files.objects.get(id=int(fid))
    fname=file.fname
    os.remove(os.path.join(settings.MEDIA_ROOT, f'{rid}/{fname}'))
    print('文件删除成功')
    file.delete()
    print('文件数据库记录删除成功')
    return JsonResponse({'code':200,'msg':'删除成功'})


def leave(request):
    # r.flushdb()
    uid=request.session.get('uid')
    rid=request.session.get('rid')
    r.set(f'user{uid}_room{rid}_files',0)
    r.set(f'user{uid}_room{rid}_record',0)
    r.set(f'user{uid}_room{rid}_users',0)
    # ru=RoomUser.objects.get(room_id=rid,user_id=uid)
    # ru.delete()
    return JsonResponse({'code':0})