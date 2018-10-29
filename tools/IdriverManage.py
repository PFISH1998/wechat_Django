from tools.webcontent import Driver
from selenium.common import exceptions


class Search:

    def time_table(self, id, pwd):
        d = Driver(id, pwd)
        try:
            d.open_page()
            html = d.get_timetable()
            term, result = d.get_timetable_result(html)
            print(result)
        except exceptions.UnexpectedAlertPresentException:
            print('学号或密码错误')
            return
        finally:
            d.driver.quit()

    def term_grade(self, id, pwd):
        listData1 = []
        listData2 = []
        try:
            d = Driver(id, pwd)
            try:
                d.open_page()
                html = d.get_grade()
                data = d.get_grade_result(html)
                if len(data) != 2:
                    listData1 = data[0]
                    listData2 = data[1]
                elif len(data) == 1:
                    listData1 = data[0]
                print(listData1, listData2)
                return
            except exceptions.UnexpectedAlertPresentException:
                print('学号或密码错误')
                return
            except TypeError:
                print('获取成绩失败')
            except exceptions.WebDriverException as e:
                print('selenium error 1', e)
            finally:
                print('销毁')
                d.driver.quit()
        except exceptions.WebDriverException:
            print('selenium error')






