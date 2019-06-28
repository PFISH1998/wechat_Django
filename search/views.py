# -*- coding: utf-8 -*-

import gc
import json
from requests import exceptions

from django.http import HttpResponse
from django.utils.timezone import now
from django.contrib.auth.models import User

from tools.dean import *
from tools.hnsxy import ShangXueYuan
from tools.biying import request_api


def index(request):

    # data = json.loads(request.body.decode('utf-8'))
    # sid = data.get('sid')
    # pwd = data.get('sid')
    # print(sid, pwd)
    return HttpResponse('Django  Welcome')


def home(request):
    try:
        bing = request_api()
        return HttpResponse(json.dumps({
            "data": bing
        }))
    except:
        return HttpResponse(status=400)


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
                result = user.update(password=pwd, last_login=now())
            else:
                result = user.create(username=sid, password=pwd, last_login=now())
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
        print(sid)
        try:
            if not cidp(sid):
                s = ShangXueYuan(sid, pwd)
                term_data = s.get_grade_sxy()
            else:
                grade, term = get_grade_result(sid, pwd)
                term_data = grade_process(grade, term)
            print("查询成功返回")
            try:
                user = User.objects.filter(username=sid)
                if user.exists():
                    user.update(password=pwd, last_login=now())
                else:
                    user.create(username=sid, password=pwd, last_login=now())
                    # return HttpResponse('nouser')
            except Exception as e:
                print('database', e)
            finally:
                return HttpResponse(json.dumps({
                    'data': term_data,
                    'code': 200,
                }))

        except exceptions.ConnectionError as e:
            print('网络连接出错', e)

        except Exception as e:
            if str(e) == 'PasswordError':
                print('密码错误', e)
                return HttpResponse(json.dumps({
                        'code': 300,
                        'info': '密码错误，请输入办事大厅密码'
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
                    'info': '获取成绩失败，请稍后重试'
                }))

    except Exception as e:
        print("其他问题", e)
        info = '可能是教务处出错了，正在解决'
        if e == 'login404':
            info = '密码出错或者其他原因'
        return HttpResponse(json.dumps({
                'code': 1013,
                'info': info
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
        print(sid)
        try:
            if cidp(sid):
                data = get_time_table_result(sid, pwd)
                result = time_table_process(data)
            else:
                s = ShangXueYuan(sid, pwd)
                result = s.get_table_sxy()
            try:
                user = User.objects.filter(username=sid)
                if user.exists():
                    user.update(password=pwd, last_login=now())
                else:
                    user.create(username=sid, password=pwd)
                    # return HttpResponse('nouser')
            except Exception as e:
                print('database', e)
            finally:
                print('查询成功返回')
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
            if str(e) == 'PasswordError' or 'login404':
                print('密码错误', e)
                return HttpResponse(json.dumps({
                    'code': 300,
                    'info': '密码错误，请输入办事大厅密码'
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
                    'info': '获取课表失败，请稍后重试'
                }))

    except Exception as e:
        print("其他问题", e)
        return HttpResponse(json.dumps({
            'code': 3025,
            'info': '可能是教务处出问题了...'
        }))
    finally:
        gc.collect()
        print('完成')

