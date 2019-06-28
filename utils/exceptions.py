# -*- coding: utf-8 -*-

class DataError(Exception):
    MESSAGE = "异常"
    ERROR_CODE = '10000'

    def __init__(self, *args):
        super(DataError, self).__init__(*args)
        self.code = self.ERROR_CODE

        # 参数位置 0 为异常 MESSAGE
        self.message = self.MESSAGE if len(args) == 0 else args[0]

        # 参数位置 1 为发生异常后返回的数据
        self.data = None if len(args) < 2 else args[1]


class PassWordError(DataError):
    MESSAGE = "密码错误"
    ERROR_CODE = '00001'


class UserNameError(DataError):
    MESSAGE = "用户不存在错误"
    ERROR_CODE = '00002'


class DeanConnectError(DataError):
    MESSAGE = "教务处连接出错"
    ERROR_CODE = '00003'


class TimeTableError(DataError):
    MESSAGE = "获取课表出错"
    ERROR_CODE = '00004'


class GradeResultError(DataError):
    MESSAGE = "获取成绩出错"
    ERROR_CODE = '00005'


