# -*- coding: utf8 -*-

import sys, os
from os.path import dirname
sys.path.insert(0, dirname(dirname(os.path.abspath(__file__))))
import argparse
from simplejson import loads
import pandas as pd
from pprint import pprint

from libs.mysql_mod import yhdb
from consts import macd_file_dir
from sell_signals.base import SellSignal
from indicator import Indicator, point_prosess_v2

from pandas_db import yhdb as pandas_yhdb


def ifcode_day_map(ifcode):
    sql = '''select distinct date(`time`) from %s;''' % ifcode
    rs = yhdb(sql)
    return [d[0].strftime('%Y-%m-%d') for d in rs]


def read_df(path):
    df_list = loads(open(path).read())
    return pd.DataFrame(df_list, columns=['time_index', 'price',
                                          'ema_short', 'ema_long',
                                          'macd_dif', 'macd_dem'])

def get_data(ifcode, thedate):
    where = '''%s where (`time` >= '%s 09:15:00' and `time` <= '%s 11:30:00')
               or (`time` >= '%s 13:00:00' and `time` <= '%s 15:15:00')''' % (ifcode, thedate, thedate, thedate, thedate)
    sql = '''select `inserttime`, DATE_FORMAT(`time`, '%Y-%m-%d %H:%i:%s') as time_index, `now` as price,
             `volume`, `hold`
             from ''' + where + ''' order by time_index;'''
    df = pd.read_sql(sql, pandas_yhdb)
    return df

def macd_df(_df, period_short, period_long, period_dif=9):
    df = point_prosess_v2(_df, 59)
    df['ma_short'] = Indicator.ewma_metric(period_short, df[['price']], 'price')
    df['ma_long'] = Indicator.ewma_metric(period_long, df[['price']], 'price')
    df['macd_dif'] = df['ma_short'] - df['ma_long']
    df['macd_dem'] = Indicator.ewma_metric(period_dif, df[['macd_dif']], 'macd_dif')

    return df


def get_all_trans(ifcode, period_short, period_long, ammout=1):
    rs = []
    total = 0
    pos_num = 0
    nag_num = 0
    trans_all = 0
    date_list = ifcode_day_map(ifcode)
    for day in date_list:
        _df = get_data(ifcode, day)
        df = macd_df(_df, period_short, period_long)
        sig_infos = SellSignal.compare_macd(df, 2, 25)
        profit_infos = SellSignal.profit_infos(sig_infos)
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


def get_first_trans(ifcode, period_short, period_long):
    rs = []
    total = 0
    pos_num = 0
    nag_num = 0
    date_list = ifcode_day_map(ifcode)
    for day in date_list:
        _df = get_data(ifcode, day)
        df = macd_df(_df, period_short, period_long)
        sig_infos = Signal.compare_macd(df, 2, 30)
        profit_infos = SellSignal.profit_infos(sig_infos)
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


def main(ifcode, period_short, period_long, amout):
    #get_first_trans(ifcode, period_short, period_long)
    get_all_trans(ifcode, period_short, period_long, amout)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="macd profit report")
    parser.add_argument("ifcode", type=str, help="ifcode")
    parser.add_argument("period_short", type=int, help="short period")
    parser.add_argument("period_long", type=int, help="long period")
    parser.add_argument("amout", type=int, help="amout")
    args = parser.parse_args()
    ifcode = args.ifcode
    period_short = args.period_short
    period_long = args.period_long
    amout = args.amout
    main(ifcode, period_short, period_long, amout)
