# -*- coding: utf8 -*-

import sys, os
from os.path import dirname
sys.path.insert(0, dirname(dirname(os.path.abspath(__file__))))
import argparse
from simplejson import loads
import pandas as pd
from pprint import pprint

from libs.mysql_mod import yhdb
from models.api.backtest.analysis import DataAnalyzer

from pandas_db import yhdb as pandas_yhdb


def ifcode_day_map(ifcode):
    sql = '''select distinct date(`time`) from %s;''' % ifcode
    rs = yhdb(sql)
    return [d[0].strftime('%Y-%m-%d') for d in rs]


def get_all_trans(ifcode, ammout=1):
    rs = []
    total = 0
    pos_num = 0
    nag_num = 0
    trans_all = 0
    date_list = ifcode_day_map(ifcode)
    for day in date_list:
        profit_infos = DataAnalyzer.boll(day, ifcode)
        profit_all = 0
        trans_num = (len(profit_infos) - 1) / 2
        trans_all += trans_num
        for item in profit_infos:
            if item['gain'] != '-':
                profit_all += int(item['gain']) * ammout
        rs.append({day: profit_all, 'trans_num': trans_num})
        total += profit_all
        if profit_all >= 0:
            pos_num += 1
        elif profit_all < 0 :
            nag_num += 1

    pprint(rs)
    print '%s total: %s' % (ifcode, total)
    print '%s profit rate: %.2f' % (ifcode, pos_num*1.0/nag_num)
    print '%s trans all number: %s' % (ifcode, trans_all)
    print '%s fees : %s' % (ifcode, trans_all * 2300)
    print '%s real profit : %s' % (ifcode, total - trans_all * 2300)


def get_first_trans(ifcode):
    rs = []
    total = 0
    pos_num = 0
    nag_num = 0
    date_list = ifcode_day_map(ifcode)
    for day in date_list:
        profit_infos =  DataAnalyzer.boll(day, ifcode)
        profit_first = 0
        for item in profit_infos:
            if item['gain'] != '-':
                profit_first = int(item['gain'])
                break
        rs.append({day: profit_first})
        if profit_first >= 0:
            pos_num += 1
        elif profit_first < 0 :
            nag_num += 1

    print '每天第一笔交易'
    pprint(rs)
    print '%s profit rate: %.2f' % (ifcode, pos_num*1.0/nag_num)


def main(ifcode):
    #get_first_trans(ifcode, period_short, period_long)
    get_all_trans(ifcode)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="macd profit report")
    parser.add_argument("ifcode", type=str, help="ifcode")
    args = parser.parse_args()
    ifcode = args.ifcode
    main(ifcode)
