import hashlib

import simplejson
from django.http import HttpResponse
from django.shortcuts import render
import json
# Create your views here.
from userapp.models import User


def login(request):
    if request.method == "GET":
        # 检查session和cookies如果已登录直接跳转聊天室列表页面
        if request.session.get('username') or request.COOKIES.get('username'):
            print('session.', request.session.get('username'))
            return render(request, 'index.html')
        else:#未登录跳转登录页面
            return render(request,'userapp/login.html')
    elif request.method == "POST":
        # 获取json信息
        request_json=simplejson.loads(request.body.decode())
        name = request_json.get('username')
        pwd = request_json.get('password')
        #checkbox 记住密码
        print(name, pwd)
        # 对密码编码
        m=hashlib.md5()
        m.update(pwd.encode())
        pwd=m.hexdigest()
        try:
            user=User.objects.get(username=name)
        except Exception as e:
            print('登录时出错',e)
            return HttpResponse(json.dumps({'code': '42', "msg": "无此用户"}))
        if user.password==pwd:
            request.session['username'] = name
            request.session['uid'] = user.id
            return HttpResponse(json.dumps({'code': '20', "msg": "登录成功"}))
        else:
            return HttpResponse(json.dumps({'code': '43', "msg": "用户名或密码错误"}))

def check_username(username):
    user = User.objects.filter(username=username)
    if user:
        return user
    else:
        return False

def register(request):
    if request.method == "POST":
        # 获取数据
        request_json=simplejson.loads(request.body.decode())
        print(request_json)
        uname = request_json.get("uname")
        pwd = request_json.get("password")
        repwd = request_json.get('repassword')
        telnumber = request_json.get("telnumber")
        print(uname, pwd, repwd,telnumber)
        # 数据检查
        if pwd!=repwd:
            return HttpResponse(json.dumps({'code':'40','msg':'两次输入密码不同'}))
        elif check_username(uname):
            return HttpResponse(json.dumps({'code': '41', 'msg': '用户名已存在'}))
        # 密码加密存储
        m=hashlib.md5()
        m.update(pwd.encode())
        password=m.hexdigest()
        # 信息存入数据库
        try:
            user=User.objects.create(username=uname,password=password,telnumber=telnumber)
        except Exception as e:
            print('存入数据错误',e)
            return HttpResponse(json.dumps({'code':'41','msg':'用户名已存在'}))
        # 写入session
        request.session['uid'] = user.id
        request.session['username'] = uname
        return HttpResponse(json.dumps({"code": '200', "msg": "注册成功"}))
    elif request.method == "GET":
        return render(request,'userapp/register.html')


def register_check(request):
    request_json=simplejson.loads(request.body.decode())
    uname=request_json['uname']
    # uname = request.json.get("uname")
    if not check_username(uname):
        return HttpResponse(json.dumps({"code": '20', "msg": "用户名可以使用"}))
    else:
        return HttpResponse(json.dumps({"code": '40', "msg": "用户名已存在"}))


def logout(request):
    del request.session['username']
    return HttpResponse(json.dumps({"code": '20', "msg": "已退出"}))


def modify(request):
    #修改用户信息
    request_json=simplejson.loads(request.body.decode())
    uname = request_json.get("username")
    pwd = request_json.get("password")
    repwd = request_json.get('repassword')
    telnumber = request_json.get("tel")
    print(uname, pwd, repwd,telnumber)
    user=check_username(uname)
    # 数据检查
    if pwd!=repwd:
        return HttpResponse(json.dumps({'code':'40','msg':'两次输入密码不同'}))
    elif len(user)!=1:
        return HttpResponse(json.dumps({'code': '41', 'msg': '用户名已存在'}))
    # 密码加密存储
    m=hashlib.md5()
    m.update(pwd.encode())
    password=m.hexdigest()
    # 信息存入数据库
    try:
        
        user.update(username=uname)
        user.update(password=password)
        user.update(telnumber=telnumber)
    except Exception as e:
        print('修改数据错误',e)
        return HttpResponse(json.dumps({'code':'41','msg':'修改信息失败'}))
    # 写入session
    request.session['username'] = uname
    return HttpResponse(json.dumps({"code": '200', "msg": "修改成功"}))


