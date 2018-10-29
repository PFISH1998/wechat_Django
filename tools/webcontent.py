from selenium import webdriver

import random
import time
import re


class Driver:

    def __init__(self, sid, pwd):
        # 启动 Firefox , 可优化
        t = time.time()
        options = webdriver.FirefoxOptions()
        options.set_headless()
        options.add_argument('--disable-gpu')
        driver = webdriver.Firefox(firefox_options=options)
        print('driver', time.time() - t)
        driver.get('http://jwauth.cidp.edu.cn/Login.aspx')
        name = driver.find_element_by_name('TextBoxUserName')
        password = driver.find_element_by_name('TextBoxPassword')
        name.clear()
        password.clear()
        name.send_keys(sid)
        password.send_keys(pwd)
        driver.find_element_by_name('ButtonLogin').click()
        self.driver = driver
        print('openpage', time.time() - t)

    def open_page(self):
        t = time.time()
        jw_url = "http://jwauth.cidp.edu.cn/NoMasterJumpPage.aspx?URL=JWGL"
        self.driver.get(jw_url)
        print('login', time.time() - t)

    def get_grade(self):
        t = time.time()
        mark_url = 'http://jw.cidp.edu.cn/Teacher/MarkManagement/StudentAverageMarkSearchFZ.aspx'
        self.driver.get(mark_url)
        print('gradepage', time.time() - t)
        # 显性等待，(driver, 超时时长， 调用频率， 异常忽略)
        # WebDriverWait(driver, 15, 0.5).until(EC.frame_to_be_available_and_switch_to_it('year1'))
        grade_html = self.driver.find_element_by_id('DivCon2').get_attribute('innerHTML')
        print('find', time.time() - t)
        # driver.find_element_by_id('year1').click()
        # HTML = driver.find_element_by_id('DivCon2')
        self.driver.quit()
        return grade_html

    def get_timetable(self):
        t = time.time()
        table_url = 'http://jw.cidp.edu.cn/Student/CourseTimetable/MyCourseTimeTable.aspx'
        self.driver.get(table_url)
        time.sleep(3)
        # term = self.driver.find_element_by_id('lblSemester').get_attribute('innerHTML')
        iframe = self.driver.find_element_by_id('iframeTimeTable')
        self.driver.switch_to_frame(iframe)
        table_html = self.driver.find_element_by_id('tableMain').get_attribute('innerHTML')
        print('find', time.time() - t)
        self.driver.quit()
        return table_html

    def get_grade_result(self, html):
        result = re.compile(r'.*?([\u4e00-\u9fa5]+).*?<tr><td(.*?)</tbody></table>.*?', re.S).findall(html)

        term = []
        for terms in result:
            lists = []
            mark = re.compile(r'.*?">(.*?)</td>.*?', re.S).findall(terms[1])
            # lists.append(term)
            l = [i for i in mark]
            for list in [l[i:i + 9] for i in range(0, len(l), 9)]:
                dict = {}
                dict['code'] = list[0]
                dict['name'] = list[1]
                dict['property_name'] = list[2]
                dict['number'] = list[3]
                dict['credit'] = list[4]
                dict['mark_value'] = list[5]
                dict['GPA'] = list[6]
                dict['ranking'] = list[7]
                lists.append(dict)
            term.append(lists)
        return term

    @staticmethod
    def get_timetable_result(self, html):
        result = re.compile(r'.*?<tr>(.*?)</tr>.*?', re.S).findall(html)
        # term = re.compile(r'(.*?)学期', re.S).findall(html)[0]+'学期'
        term = []
        list = []
        class_list = []
        class_set = []
        # 这几行是保存信息
        n = [1, 3, 6, 8, 11]
        m = 0

        # 留下有用行
        for i in result:
            if m in n:
                list.append(i)
            m += 1

        # 匹配每行中的有课部分
        for index in list:
            class_name = re.compile(r'.*?rowspan="(.*?)">.*?').findall(index)
            class_set.append(class_name)

            for content in list:
                data = re.compile(r'.*?<td rowspan="[2-4]">(.*?)</td>', re.S).findall(content)
                # print('data', data)
                for i in data:
                    dict = {}
                    cname = re.compile(r'class="spLUName">《(.*?)》</span>').findall(i)
                    week_info = re.compile(r'class="spWeekInfo">(.*?)</span>').findall(i)
                    room = re.compile(r'class="spClassroom">(.*?)</span>').findall(i)
                    teacher = re.compile(r'class="spTeacherName">(.*?)</span>').findall(i)
                    building = re.compile(r'class="spBuilding">(.*?)</span>').findall(i)
                    method = re.compile(r'class="spDelymethodName.*?>(.*?)</span>').findall(i)

                    # print(cname, room, week,teacher)
                    dict['class_name'] = cname[0]
                    dict['class_room'] = room[0]
                    dict['week_info'] = week_info[0]
                    dict['teacher'] = teacher[0]
                    dict['building'] = building[0]
                    dict['method'] = method[0]
                    dict['color'] = random.randint(0, 12)

                    if len(cname) == 2:
                        dict['class_room2'] = room[1]
                        dict['building2'] = building[1]
                        dict['week_info2'] = week_info[1]
                    class_list.append(dict)

        m = 0
        n = 0
        week = []
        # 遍历分布的二维数组，将其与课程对应
        for a in class_set:
            # q是计数 a 中 list 的下标，w是class_set中a的下标
            q = 0
            w = 0
            classes = []

            # 4的位置下方插入 x
            for i in a:
                if i == '4':
                    class_set[m + 1].insert(q, 'x')
                q += 1

            # 填满周六 周日
            if 7 >= len(a):
                for x in range(7 - len(a)):
                    a.append('1')

            # print('len', a)
            for i in a:
                # print(i)
                # 2 为有课位置，将其代替成数据，1 放入空 dict, 4是两节大课的位置
                if i == '2' or i == '4':
                    class_dict = class_list[n]
                    n += 1

                # 当位置为x，数据参照上一个list相同位置
                elif i == 'x':
                    class_dict = week[m-1][w]
                else:
                    class_dict = {'class': 'none'}
                classes.append(class_dict)

                w += 1
            m += 1
            week.append(classes)

            # 分布的数组变成了一周的数据

        # print(week)
        search_result = []
        # 用7个 list 来装七天的数据， 将按时间分布的信息转置成按星期分布
        c = 0
        for i in range(len(a)):
            m = []
            for a in week:
                m.append(a[c])
            search_result.append(m)
            c += 1
        grade_result = search_result
        # print('grade', grade_result)

        return grade_result
