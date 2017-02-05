# -*- coding: utf8 -*-

import sys, os
from os.path import dirname
sys.path.insert(0, dirname(dirname(os.path.abspath(__file__))))
import argparse
import simplejson

from consts import macd_param_analysis_dir
from models.api.backtest.analysis import DataAnalyzer


def params_conbination():
    rs = {}
    pre_offset = 10
    pre_point = 7
    pre_time = 20

    offset_list = []
    point_list = []
    time_list = []
    while pre_offset <= 30:
        offset_list.append(pre_offset)
        pre_offset += 2

    while pre_point <= 10:
        point_list.append(pre_point)
        pre_point += 1

    while pre_time <= 59:
        time_list.append(pre_time)
        pre_time += 2


    for _p in time_list:
        for _f in offset_list:
            for _pp in point_list:
                rs['time:%s  offset:%s point:%s' % (_p, _f, _pp)] = [_p, _f, _pp]
    return rs


def analysis_by_param(params_conbine, ifcode, period_short, period_long, trans_amount):
    rs = {}
    for param, v in params_conbine.items():
        pre_time = v[0]
        pre_offset = v[1]
        pre_point = v[2]
        print '************'
        print param
        rs[param] = DataAnalyzer.macd_if_analysis(ifcode, pre_point, pre_time, pre_offset, \
                         period_short=12, period_long=26, period_dif=9)

    _file = '%s/%s' % (macd_param_analysis_dir, ifcode)
    f = open(_file, 'w')
    f.write(simplejson.dumps(rs))
    f.close()


def main(ifcode, period_short, period_long, trans_amount):
    params_conbine = params_conbination()
    analysis_by_param(params_conbine, ifcode, period_short, period_long, trans_amount)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="macd metric params maker")
    parser.add_argument("ifcode", type=str, help="ifcode")
    parser.add_argument("period_short", type=int, help="short period")
    parser.add_argument("period_long", type=int, help="long period")
    parser.add_argument("amount", type=int, help="amount")
    args = parser.parse_args()
    ifcode = args.ifcode
    period_short = args.period_short
    period_long = args.period_long
    amount = args.amount
    main(ifcode, period_short, period_long, amount)
