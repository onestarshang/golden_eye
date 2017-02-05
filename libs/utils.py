# -*- coding: utf8 -*-

from datetime import datetime, timedelta, date, time as datetime_time
from simplejson import dumps
from functools import wraps
from time import mktime
from consts import jiaoge
from libs.mysql_mod import yhdb


DATE_DISPLAY_FORMAT = '%Y-%m-%d'
DATE_RAW_FORMAT = '%Y%m%d'


def day2int(d):
    return mktime(d.timetuple())*1000


def default(o):
    if isinstance(o, datetime):
        return '%s' % o.strftime('"%Y-%m-%d %H:%M:%S"')
    if isinstance(o, datetime_time):
        return '%s' % o.strftime('"%H:%M:%S"')
    if isinstance(o, date):
        return '%s' % o.strftime('"%Y-%m-%d"')
    raise TypeError(repr(o) + " is not JSON serializable")


def jsonize(func):
    @wraps(func)
    def _(*a, **kw):
        r = func(*a, **kw)
        return dumps(r, default=default)
    return _


def default_begin_date(end_date):
    return days_ago(5, day=end_date)


def get_date_range(args):
    yesterday = days_ago(1)
    end = args.get('end_date') or yesterday
    begin = args.get('begin_date') or default_begin_date(end)
    return begin, end


def display_date(d):
    input_type = type(d)
    if input_type == int:
        return timestamp2display_date(d)
    elif input_type in (str, unicode):
        return day2str(str2day(d), DATE_DISPLAY_FORMAT)
    elif input_type in (date, datetime):
        return d.strftime(DATE_DISPLAY_FORMAT)
    else:
        try:
            return day2str(str2day(d), DATE_DISPLAY_FORMAT)
        except:
            return 'invalid date type'


def day2str(day, format=DATE_RAW_FORMAT):
    return day.strftime(format)


def str2day(day, format=DATE_RAW_FORMAT):
    return datetime.strptime(day, format)


def timestamp2display_date(timestamp):
    return datetime.fromtimestamp(timestamp).strftime(DATE_DISPLAY_FORMAT)


def days_ago(n, day=None):
    if not day:
        day = datetime.today()
    elif type(day) in (str, unicode):
        day = str2day(day)
    return day2str(day - timedelta(n))


def get_ifcode(today):
    ifcode = 'if1601'
    for _ifcode, date_range in jiaoge.items():
        if today >= date_range[0] and today <= date_range[1]:
            ifcode = _ifcode
            break
    return ifcode


def get_week_day(today):
    week_day = today.weekday()
    if week_day == 5:
        return today - timedelta(days=1)
    elif week_day == 6:
        return today - timedelta(days=2)
    else:
        return today


def ifcode_day_map(ifcode):
    sql = '''select distinct date(`time`) from %s order by `time` desc;''' % ifcode
    rs = yhdb(sql)
    return [d[0].strftime('%Y-%m-%d') for d in rs]


def pre_day(today):
    week_day = today.weekday()
    if week_day == 0:
        return today - timedelta(days=3)
    else:
        return today - timedelta(days=1)
    return today
