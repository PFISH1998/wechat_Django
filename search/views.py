from django.shortcuts import render
from django.http import HttpResponse
from tools.dean import get_grade_result, grade_process
from tools.webcontent import Driver
from selenium.common import exceptions
import requests
import json
import time


# Create your views here.

def index(request):
    # data = json.loads(request.body.decode('utf-8'))
    # sid = data.get('sid')
    # pwd = data.get('sid')
    # print(sid, pwd)
    return HttpResponse('Django test Welcome')


def grade(request):
    try:
        body = json.loads(request.body.decode('utf-8'))
        sid = body.get('sid')
        pwd = body.get('pwd')
        try:
            grade, term = get_grade_result(sid, pwd)
            term_data = grade_process(grade, term)
            print("返回")
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
        print('完成')


def calendar(request, sid, pwd):
    pass


def time_table(request):
    body = json.loads(request.body.decode('utf-8'))
    sid = body.get('sid')
    pwd = body.get('pwd')
    term = []
    result = []
    print(sid, pwd, 'timetable')
    d = Driver(sid, pwd)
    try:
        try:
            d.open_page()
            html = d.get_timetable()
            result = d.get_timetable_result(html)
            print(result)
            return HttpResponse(
                json.dumps({
                    'term': term,
                    'data': result,
                    'code': 200
                }))
        except exceptions.UnexpectedAlertPresentException:
            print('学号或密码错误')
            return HttpResponse(
                json.dumps({
                    'code': 300,
                }))
        except TypeError as e:
            print('获取课表失败, type error', e)
            return HttpResponse(
                json.dumps({
                    'code': 1000,
                    'info': '获取课表失败，请稍后重试'
                }))
        except exceptions.WebDriverException as e:
            print('selenium error2, dean problem', e)
            return HttpResponse(
                json.dumps({
                    'code': 1001,
                    'info': '服务器出现了问题'
                }))
        finally:
            print('销毁进程')
            d.driver.quit()
    except exceptions.WebDriverException as e:
        print('selenium error1, network problem', e)
        return HttpResponse(
            json.dumps({
                'code': 1002,
                'info': '服务器出现了问题'
            }))
    finally:
        print('销毁进程')
        d.driver.quit()
