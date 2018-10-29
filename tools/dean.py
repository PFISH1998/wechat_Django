import json
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
    # fun(165042204, 19971216)
    fun(165041131, 19981202)
    print(time.time() - t)


def open_page(sid, pwd):
    s = requests.Session()
    t = s.get(login_url.format(sid, pwd))
    t.encoding = 'utf-8'
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
    # print(json.loads(str(grade_info)))
    print(json.loads(grade_info))
    print(json.loads(semester_year))

    return json.loads(grade_info), json.loads(semester_year)


#
# @time_test
def get_time_table_result(sid, pwd):
    s = open_page(sid, pwd)
    x = s.post(table_url, data=time_table_data)
    data = json.loads(x.text)
    x.encoding = 'ISO-8859-1'
    print(data)


def grade_process(grade, term):
    for year in term:
        # print(year)

        for i in year['List']:
            # print(i['SemesterId'])
            grade_list = []
            for g in grade:
                # print("g     ", g['SemesterID'], i['SemesterId'])
                if int(g['SemesterID']) == int(i['SemesterId']):
                    g.update({'Credit': g['Credit'][:3]})
                    grade_list.append(g)
            i.update({'grade_list': grade_list})
    return term
