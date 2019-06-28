# -*- coding: utf-8 -*-

from lxml import etree
import random
import json
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import requests


login_url = 'http://jwauth.cidp.edu.cn/Login.ashx?name={}&pwd={}&action=loginJsonP'
jw_index_url = 'http://jwauth.cidp.edu.cn/Student/MyAcademicCareer.aspx'
my_jw_url = 'http://jwauth.cidp.edu.cn/NoMasterJumpPage.aspx?URL=JWGL'

grade_url = 'http://jw.cidp.edu.cn/Teacher/MarkManagement/StudentAverageMarkSearchFZ.aspx'
table_url = 'http://jw.cidp.edu.cn/Teacher/TimeTableHandler.ashx?r=0.6142657924934334'

ehall_url = "http://authserver.cidp.edu.cn/authserver/login?service=http%3a%2f%2fjw.cidp.edu.cn%2fLoginHandler.ashx"


time_table_data = {
    'action': 'getTeacherTimeTable',
    'isShowStudent': '1',
    'semId': '59',
    'testTeacherTimeTablePublishStatus': '1',
    'isPublic': ''
    }


def time_test(fun):
    t = time.time()
    print(time.time() - t)


# 模拟登陆页面，返回cookie
def log_in_ehall(sid, pwd):
    driver = webdriver.PhantomJS('/var/django/wechat/tools/phantomjs')
    # driver = webdriver.PhantomJS('/Users/perry/Documents/GitHub/wechat_Django/tools/phantomjsmac')
    driver.get(ehall_url)
    driver.find_element_by_id('username').send_keys(sid)
    driver.find_element_by_id('password').send_keys(pwd)
    driver.find_element_by_xpath('//*[@id="casLoginForm"]//button').click()
    try:
        WebDriverWait(driver, 3).until(
            EC.title_is('教务管理系统')
        )
    except Exception as e:
        raise Exception('PasswordError')
    else:
        cookies = driver.get_cookies()
        return cookies
    finally:
        driver.quit()


# 构造带 cookie 的请求
def set_cookie(cookies):
    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])
    return s


# def open_page(sid, pwd):
#     s = requests.Session()
#     t = s.get(login_url.format(sid, pwd))
#     t.encoding = 'utf-8'
#     msg = json.loads(t.text[1:-1])['Message']
#     if msg == '密码不正确':
#         raise Exception('PasswordError')
#     s.get(jw_index_url)
#     s.get(my_jw_url)
#     return s

def open_page(sid, pwd):
    cookies = log_in_ehall(sid, pwd)
    return set_cookie(cookies)


# @time_test
def get_grade_result(sid, pwd):
    s = open_page(sid, pwd)
    grade_page = s.get(grade_url).text
    data = etree.HTML(grade_page)
    semester_year = data.xpath('//input[@id="hfSemesterFramework"]/@value')[0]
    grade_info = data.xpath('//input[@id="hfAverageMarkFromClass"]/@value')[0]
    return json.loads(grade_info), json.loads(semester_year)


#
# @time_test
def get_time_table_result(sid, pwd):
    s = open_page(sid, pwd)
    x = s.post(table_url, data=time_table_data)
    data = json.loads(x.text)
    x.encoding = 'ISO-8859-1'
    return data


def grade_process(grade, term):
    for year in term:
        for i in year['List']:
            grade_list = []
            for g in grade:
                if int(g['SemesterID']) == int(i['SemesterId']):
                    g.update({'Credit': g['Credit'][:3]})
                    grade_list.append(g)
            i.update({'grade_list': grade_list})
    return term


def sort_list(week_day):
    time_spend_dict = {22: 200, 48: 400}
    course_start_dict = {96: 0, 122: 1, 168: 2, 194: 3, 228: 4}
    for i in week_day:
        time_value = i['TimeSlotEnd'] - i['TimeSlotStart']
        time_spend = time_spend_dict.get(time_value, 400)
        i.update({'time_spend': time_spend})

        course_index = course_start_dict.get(i['TimeSlotStart'], 0)
        i.update({'course_index': course_index})
        i.update({'color': random.randint(0, 12)})

        del i['DCId'], i['DCPId'], i['TimeSlotStart'], i['TimeSlotEnd'], i['Capacity']
        del i['DCSN'], i['Count'], i['WeekInterval'], i['WeekStart'], i['WeekEnd'],
        del i['LUCode'], i['ClassCodes'], i['TeacherRollNumber']

    other_list = []
    for index in range(6):
        same_list = []
        for item in week_day:
            if item['course_index'] == index:
                # print(len(same_list))
                same_list.append(item)
            if len(same_list) > 1:
                same_list[0].update({'FullName2': same_list[1]['FullName']})
                same_list[0].update({'LUName2': same_list[1]['LUName']})
                same_list[0].update({'Building2': same_list[1]['Building']})
                same_list[0].update({'Classroom2': same_list[1]['Classroom']})
                same_list[0].update({'DelymethodName2': same_list[1]['DelymethodName']})
                same_list[0].update({'Remark2': same_list[1]['Remark']})
        if same_list:
            other_list.append(same_list[0])

    new_list = sorted(other_list, key=lambda e: e.__getitem__('course_index'))
    return new_list


def time_table_process(data):
    data_list = []
    week = ['OnMonday', 'OnTuesday', 'OnWednesday', 'OnThursday', 'OnFriday', 'OnSaturday', 'OnSunday']
    # print(course)
    # 循环一周
    # 判断是否为当天，是的话加入一天的序列
    for t in week:
        week_day = []
        for course in data['Data']:
            if course[t]:
                week_day.append(course)
        for c in data['Data']:
            del c[t]
        data_list.append(sort_list(week_day))
    return data_list


def cidp(sid):
    if len(sid) == 8 and sid.startswith("180"):
        return True
    elif sid[2] == '5':
        return True
    else:
        return False


