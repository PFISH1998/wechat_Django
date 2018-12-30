import gc
import time

from django.shortcuts import render
from django.http import HttpResponse
from tools.dean import get_grade_result, grade_process, get_time_table_result, time_table_process
from django.contrib.auth.models import User
import requests
import json


# Create your views here.
from tools.one import One


def index(request):

    # data = json.loads(request.body.decode('utf-8'))
    # sid = data.get('sid')
    # pwd = data.get('sid')
    # print(sid, pwd)
    return HttpResponse('Django test Welcome')


def home(request):
    o = One()
    daily = o.get_page()
    return HttpResponse(json.dumps({
        "data": daily
    }))


def register(request):
    try:
        # body = json.loads(request.body.decode('utf-8'))
        body = request.POST
        sid = body.get('username')
        pwd = body.get('password')
        print(sid, pwd)
        try:

            user = User.objects.filter(username=sid)
            if user.exists():
                result = user.filter(username=sid).update(password=pwd)
            else:
                result = user.create(username=sid, password=pwd)
                # return HttpResponse('nouser')
        except Exception as e:
            print('database', e)
        finally:
            return HttpResponse(json.dumps({
                'user': sid,
                'pwd': pwd,
                'result': result
            }))

    except Exception as e:
        print('exception', e)
        return HttpResponse(json.dumps({
            'error': e
        }))
    finally:
        gc.collect()


def grade(request):
    try:
        body = json.loads(request.body.decode('utf-8'))
        sid = body.get('sid')
        pwd = body.get('pwd')
        try:
            grade, term = get_grade_result(sid, pwd)
            term_data = grade_process(grade, term)
            print("返回")
            try:
                user = User.objects.filter(username=sid)
                if user.exists():
                    user.filter(username=sid).update(password=pwd)
                else:
                    user.create(username=sid, password=pwd)
                    # return HttpResponse('nouser')
            except Exception as e:
                print('database', e)
            finally:
                return HttpResponse(json.dumps({
                    'data': term_data,
                    'code': 200,
                }))

        except requests.exceptions.ConnectionError as e:
            print('网络连接出错', e)

        except Exception as e:
            print("1", e)
            if str(e) == 'PasswordError':
                print('密码错误', e)
                return HttpResponse(json.dumps({
                        'code': 300,
                        'info': '密码错误'
                    }))

            elif str(e) == 'IdError':
                print('用户名出错', e)
                return HttpResponse(json.dumps({
                    'code': 1000,
                    'info': '用户名不存在，请您确认登录身份'
                }))
            else:
                print(e)
                return HttpResponse(json.dumps({
                    'code': 1001,
                    'info': '获取成绩失败，请稍后重试'+ e
                }))

    except Exception as e:
        print("其他问题", e)
        return HttpResponse(json.dumps({
                'code': 2222,
                'info': '奇怪的问题，正在解决'
            }))
    finally:
        gc.collect()
        print('完成')


def calendar(request, sid, pwd):
    pass


def time_table(request):
    try:
        body = json.loads(request.body.decode('utf-8'))
        sid = body.get('sid')
        pwd = body.get('pwd')
        try:
            data = get_time_table_result(sid, pwd)
            result = time_table_process(data)
            try:
                user = User.objects.filter(username=sid)
                if user.exists():
                    user.filter(username=sid).update(password=pwd)
                else:
                    user.create(username=sid, password=pwd)
                    # return HttpResponse('nouser')
            except Exception as e:
                print('database', e)
            finally:
                return HttpResponse(
                    json.dumps({
                        'data': result,
                        'code': 200
                    }))
        except requests.exceptions.ConnectionError as e:
            print('网络连接出错', e)
            return HttpResponse(
                json.dumps({
                    'info': "服务器连接出错",
                    'code': 1002
                }))

        except Exception as e:
            print("1", e)
            if str(e) == 'PasswordError':
                print('密码错误', e)
                return HttpResponse(json.dumps({
                    'code': 300,
                    'info': '密码错误'
                }))

            elif str(e) == 'IdError':
                print('用户名出错', e)
                return HttpResponse(json.dumps({
                    'code': 1000,
                    'info': '用户名不存在，请您确认登录身份'
                }))
            else:
                print(e)
                return HttpResponse(json.dumps({
                    'code': 1001,
                    'info': '获取课表失败，请稍后重试' + e
                }))

    except Exception as e:
        print("其他问题", e)
        return HttpResponse(json.dumps({
            'code': 2222,
            'info': '奇怪的问题，正在解决'
        }))
    finally:
        gc.collect()
        print('完成')
