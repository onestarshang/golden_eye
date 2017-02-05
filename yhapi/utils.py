#-*- coding: utf8 -*-

from datetime import datetime, timedelta
from mysql_mod import rundb


def _time():
    today = datetime.today().strftime('%a_%b_%d_%Y_%H:%M:%S').replace('_', '%20') + '''%20GMT+0800%20(CST)'''
    return today


def _time_trans():
    today = datetime.today().strftime('%a_%b_%d_%Y_%H:%M:%S').replace('_', '+').replace(':', '%3A') + '''+GMT%2B0800+(CST)'''
    return today


def save_data(path, data):
    f = open(path, 'w')
    try:
        f.write(data)
        f.close()
    except BaseException, e:
        f.close()
        print e


def UTC_time(time_str):
    hour, mint, sec = time_str.split(' ')[1].split(':')
    if len(hour) == 1:
        hour = '0' + hour
    elif len(mint) == 1:
        mint = '0' + mint
    elif len(sec) == 1:
        sec = '0' + sec

    tmp = time_str.split(' ')[0] + ' ' + ('%s:%s:%s' % (hour, mint, sec))
    date_time = datetime.strptime(tmp, '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
    return date_time


def ifcode_map():
    rows = rundb('''select * from dim_ifcode;''')
    ifcode_d = {}
    for item in rows:
        if 'IF15' in str(item[1]):
            ifcode_d[str(item[1])] = str(item[0])
    return ifcode_d


if __name__ == '__main__':
    #UTC_time('2015-8-11 7:14:20')
    import pprint
    pprint.pprint(ifcode_map())
    print _time_trans()
