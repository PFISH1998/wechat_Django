import json
import random

import requests
import time
import html
from lxml import etree


login_url = 'http://jwauth.cidp.edu.cn/Login.ashx?name={}&pwd={}&action=loginJsonP'
jw_index_url = 'http://jwauth.cidp.edu.cn/Student/MyAcademicCareer.aspx'
my_jw_url = 'http://jwauth.cidp.edu.cn/NoMasterJumpPage.aspx?URL=JWGL'

grade_url = 'http://jw.cidp.edu.cn/Teacher/MarkManagement/StudentAverageMarkSearchFZ.aspx'
table_url = 'http://jw.cidp.edu.cn/Teacher/TimeTableHandler.ashx?r=0.6142657924934334'


# url_3 = 'http://jw.cidp.edu.cn/Teacher/TimeTable.aspx?display=10001101100&showc=0&showsem=1&semid=58'
# s.get('http://jw.cidp.edu.cn/Student/CourseTimetable/MyCourseTimeTable.aspx')


time_table_data = {
    'action': 'getTeacherTimeTable',
    'isShowStudent': '1',
    'semId': '58',
    'testTeacherTimeTablePublishStatus': '1',
    'isPublic': ''
        }


def time_test(fun):
    t = time.time()
    print(time.time() - t)


def open_page(sid, pwd):
    s = requests.Session()
    t = s.get(login_url.format(sid, pwd))
    t.encoding = 'utf-8'
    msg = json.loads(t.text[1:-1])['Message']
    if msg == '密码不正确':
        raise Exception('PasswordError')
    s.get(jw_index_url)
    s.get(my_jw_url)
    return s


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
    for i in week_day:
        if i['TimeSlotEnd'] - i['TimeSlotStart'] == 22:
            time_spend = 200
        elif i['TimeSlotEnd'] - i['TimeSlotStart'] == 48:
            time_spend = 400
        else:
            time_spend = 200
        i.update({'time_spend': time_spend})

        if i['TimeSlotStart'] == 96:
            course_index = 0
        elif i['TimeSlotStart'] == 122:
            course_index = 1
        elif i['TimeSlotStart'] == 168:
            course_index = 2
        elif i['TimeSlotStart'] == 194:
            course_index = 3
        elif i['TimeSlotStart'] == 228:
            course_index = 4
        else:
            course_index = 0
        i.update({'course_index': course_index})
        i.update({'color': random.randint(0, 12)})

        del i['DCId'], i['DCPId'], i['TimeSlotStart'], i['TimeSlotEnd'], i['DCSN']
        del i['WeekInterval'], i['WeekStart'], i['WeekEnd'], i['Count'], i['Capacity']
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
