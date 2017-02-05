# -*- coding: utf8 -*-

from libs.mysql_mod import yhdb
from libs.utils import day2int, str2day, pre_day, DATE_DISPLAY_FORMAT, get_ifcode


def obj_to_list(obj):
    if not obj:
        return []
    return [day2int(obj.time_index), obj.price, obj.volume]


class BacktestData(object):

    def __init__(self, inserttime, time_index, price, volume):
        self.inserttime = inserttime
        self.time_index = time_index
        self.price = price
        self.volume = volume

    @classmethod
    def get_data_by_ifcode(cls, date, ifcode):
        where = '''%s where (`time` >= '%s 09:30:00' and `time` <= '%s 11:30:00')
                   or (`time` >= '%s 13:00:00' and `time` <= '%s 15:00:00')''' % (ifcode, date, date, date, date)

        sql = '''select `inserttime`, `time` as time_index, `now` as price, `volume`
                 from ''' + where + ''' order by inserttime;'''
        rs = yhdb(sql)
        return [obj_to_list(cls(*r)) for r in rs]

    @classmethod
    def get_macd_data_by_ifcode(cls, date, ifcode, pre_time):
        today = str2day(date, DATE_DISPLAY_FORMAT)
        pre = pre_day(today)
        pre_str = pre.strftime('%Y-%m-%d')
        _ifcode = get_ifcode(pre)
        # 如果是上一个合约
        _rs = []
        if _ifcode != ifcode:
            _where = '''%s where (`time` >= '%s 14:%s:00' and `time` <= '%s 15:00:00')
                       ''' % (_ifcode, pre_str, pre_time, pre_str)
            _sql = '''select `inserttime`, `time` as time_index, `now` as price, `volume`
                      from ''' + _where + ''' order by inserttime;'''
            _rs = yhdb(_sql)

        where = '''%s where (`time` >= '%s 14:%s:00' and `time` <= '%s 15:00:00')
                   or (`time` >= '%s 09:30:00' and `time` <= '%s 11:30:00')
                   or (`time` >= '%s 13:00:00' and `time` <= '%s 15:00:00')
                   ''' % (ifcode, pre_str, pre_time, pre_str, date, date, date, date)

        sql = '''select `inserttime`, `time` as time_index, `now` as price, `volume`
                 from ''' + where + ''' order by inserttime;'''

        rs = yhdb(sql)
        if _rs:
            rs = _rs + rs
        return [obj_to_list(cls(*r)) for r in rs if r]
