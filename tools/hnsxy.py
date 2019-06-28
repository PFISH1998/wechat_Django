# -*- coding: utf-8 -*-

import random

from bs4 import BeautifulSoup
import execjs
import requests


class ShangXueYuan:
    """
    实现对 湖南商学院 教务处课表、成绩的查询
    TODO：登录的判断，异常处理优化
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self._login_url = 'http://jwgl.hnuc.edu.cn/jsxsd/xk/LoginToXk'
        self._table_index_url = "http://jwgl.hnuc.edu.cn/jsxsd/xskb/xskb_list.do"
        self._index_url = "http://jwgl.hnuc.edu.cn/jsxsd/framework/xsMain.jsp"
        self._grade_url = "http://jwgl.hnuc.edu.cn/jsxsd/kscj/cjcx_list"
        self.header = {
            "Connection": "keep-alive",
            "Content-Length": "43",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "jwgl.hnuc.edu.cn",
            "Origin": "http://jwgl.hnuc.edu.cn",
            "Referer": "http://jwgl.hnuc.edu.cn/jsxsd/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/72.0.3626.119 Safari/537.36"
        }

    def _get_encode_user_and_pwd(self):
        try:
            node = execjs.get()
            file = '/var/django/wechat/tools/encode.js'
            # file = 'D:\\python\\wechat\\tools\\encode.js'
            ctx = node.compile(open(file).read())
            user = 'encodeInp("{}")'.format(self.username)
            password = 'encodeInp("{}")'.format(self.password)
            result = '{}%%%{}'.format(str(ctx.eval(user)), str(ctx.eval(password)))
            return result
        except Exception as e:
            print(e)
            raise Exception("JS出错", e)

    def _request_page_session(self, encode=""):
        if not encode:
            return
        self.session.post(url=self._login_url, headers=self.header, data={"encoded": encode}, allow_redirects=False)
        login_page = self.session.get(self._index_url)
        if login_page.status_code == 200:
            return self.session
        if login_page.status_code == 404:
            e = 'login404'
            raise Exception(e)

    def _get_table_page(self):
        table_page = self.session.get(self._table_index_url)
        return str(table_page.text)

    def _get_table_form(self):
        table_data = self._get_table_page()
        soup = BeautifulSoup(str(table_data), 'lxml')
        table = soup.select('.Nsb_r_list.Nsb_table')[0]
        tr = BeautifulSoup(str(table), 'lxml')
        # 每天第 i 节课
        table_list = []
        for td in tr.find_all('tr')[1:-1]:
            time_list = []
            # 每节课信息
            for i in td.find_all('div', class_='kbcontent'):
                # 对每节课信息进行处理
                time_list.append(list(filter((lambda s: s[0] if s[0] != '\xa0' else ''), i.strings)))
            table_list.append(time_list)
        return table_list

    # 格式化课表，返回数据
    @ staticmethod
    def _serializer_table(table_list):
        week_list = []
        for i in range(7):
            # 每天
            week_data = []
            for val in table_list:
                table_dict = dict()
                # print(val)
                if val[i]:
                    item = val[i]
                    # 定位课程
                    _class_time = ShangXueYuan._time_spend(item[4])
                    table_dict.update({
                        "Classroom": item[3],
                        "FullName": item[1],
                        "Remark": ' '.join([item[2], item[4], item[-1], item[3]]),
                        "LUName": item[0],
                    })

                    table_dict.update({"color": random.randint(0, 12)})
                    table_dict.update({"time_spend": _class_time[0], "course_index": _class_time[1]})
                    week_data.append(table_dict)
            week_list.append(week_data)
        # print(week_list)
        return week_list

    @ staticmethod
    def _time_spend(time_spend):
        _class_time = time_spend[1:-2].split("-")
        spend = (int(str(_class_time[-1])) - int(str(_class_time[0])) + 1) * 100
        course_index = int(int(str(_class_time[0]))/2)
        return spend, course_index

    # 成绩页面
    def _get_grade_index(self):
        table_page = self.session.get(self._grade_url)
        return table_page.text

    # 打开网页后拿到成绩表单
    def _get_grade_form(self):
        table_page = self._get_grade_index()
        soup = BeautifulSoup(str(table_page), 'lxml')
        grade = soup.select('.Nsb_r_list.Nsb_table')[0]
        tr = BeautifulSoup(str(grade), 'lxml')
        grade_list = []
        for td in tr.find_all('tr')[1:]:
            # 去除一些转义字符
            g_list = list(filter((lambda a: a.replace('\n', '')), td.strings))
            grade_list.append(g_list[1:])
        return grade_list

    @ staticmethod
    def _serializer_grade(grade_list):
        if not grade_list:
            e = 'NoneGradeList'
            raise Exception(e)

        # year_list = []
        semester = []
        term = []
        grade_result_list = []
        for line in grade_list:
            grade_dict = dict(
                Name=line[2],
                index="无",
                semesterYear=line[0],
                MarkValue=line[3],
                CP=line[-5],
                maxmark="-",
                minmark="-"
            )
            grade_result_list.append(grade_dict)
            semester.append(line[0][:-2])
            term.append(line[0])
        # 年份， 学期去重
        semester = list(set(semester))
        semester.sort()
        term = list(set(term))
        term.sort(reverse=True)
        # print(semester)
        # 分年， 年中的学期
        # 任性一回， 以后维护看见这行代码的同学轻点骂；datetime 2019/3/2 10:40 Sat
        # for s in semester:
        #     s_dict = dict(SemesterYear=s, List=[dict(STName=a, grade_list=list(filter((lambda g: g['semesterYear'] == a), grade_result_list))) for a in list(filter((lambda t: t[:-2] == s), term))])
        #     year_list.append(s_dict)
        # 终极无敌版
        return [dict(
            SemesterYear=sem, List=[
                dict(
                    STName=a, grade_list=list(
                        filter((lambda g: g['semesterYear'] == a), grade_result_list))) for a in list(
                    filter((lambda t: t[:-2] == sem), term))]) for sem in semester]

    # 课表对外接口
    def get_table_sxy(self):
        # js 加密数据
        js_encode = self._get_encode_user_and_pwd()
        # 登录网站
        self._request_page_session(js_encode)
        # 打开课表页面, 拿到网页内容
        table_list = self._get_table_form()
        # 格式化数据
        return self._serializer_table(table_list)

    # 成绩对外接口
    def get_grade_sxy(self):
        js_encode = self._get_encode_user_and_pwd()
        self._request_page_session(js_encode)
        grade_list = self._get_grade_form()
        return self._serializer_grade(grade_list)
