#-*- coding: utf8 -*-

import sys, os
from os.path import dirname
sys.path.insert(0, dirname(dirname(os.path.abspath(__file__))))

import time
import traceback
from datetime import datetime, timedelta, date
import simplejson

from yhapi.api_logger import yh_api_logger
from yhapi.transaction_api import yinhe_trans, yinhe_trans_check

from consts import trans_session_dir
from libs.utils import str2day

from push_it import push_sig


def create_session(ifcode, today):
    trans_session = yinhe_trans()
    if yinhe_trans_check(trans_session):
        _file = '%s/%s_%s' % (trans_session_dir, ifcode, today)
        f = open(_file, 'w')
        try:
            f.write(str(trans_session))
            f.close()
        except BaseException, e:
            print e
            f.close()
            tip = '写session 文件失败'
            push_sig(tip)
    else:
        push_sig('交易初始化，登陆失败')


def main(ifcode):
    today = date.today()
    year, month, day = today.year, today.month, today.day
    week = today.weekday()
    if week in [5, 6]:
        push_sig('周六周日不交易')
        return
    datetime_start = datetime(year, month, day, 9, 30, 00)
    datetime_end = datetime(year, month, day, 15, 00, 00)
    datetime_now = datetime.now()

    #today = date(2016, 12, 31)
    #create_session(ifcode, today)
    while True:
        try:
            if datetime_now > datetime_start and datetime_now <= datetime_end:
                try:
                    create_session(ifcode, today)
                except BaseException, e:
                    print traceback.format_exc()
            else:
                break
        except BaseException, e:
            yh_api_logger.error(traceback.format_exc())
        datetime_now = datetime.now()
        time.sleep(600)


if __name__ == '__main__':
    arg = sys.argv
    ifcode = arg[1]
    main(ifcode)
