# -*- coding: utf8 -*-

import sys, os
from os.path import dirname
sys.path.insert(0, dirname(dirname(os.path.abspath(__file__))))
import argparse
from simplejson import loads
import pandas as pd
from pprint import pprint

from libs.mysql_mod import yhdb
from consts import ema_file_dir
from sell_signals.base import SellSignal
from indicator import Indicator, point_prosess_v2

from pandas_db import yhdb as pandas_yhdb


def ifcode_day_map(ifcode):
    sql = '''select distinct date(`time`) from %s;''' % ifcode
    rs = yhdb(sql)
    return [d[0].strftime('%Y-%m-%d') for d in rs]


def read_df(path):
    df_list = loads(open(path).read())
    return pd.DataFrame(df_list, columns=['time_index', 'price', 'volume',
                                          'ema_short', 'ema_long'])


def get_data(ifcode, thedate):
    where = '''%s where (`time` >= '%s 09:30:00' and `time` <= '%s 11:30:00')
               or (`time` >= '%s 13:00:00' and `time` <= '%s 15:00:00')''' % (ifcode, thedate, thedate, thedate, thedate)
    sql = '''select `inserttime`, DATE_FORMAT(`time`, '%Y-%m-%d %H:%i:%s') as time_index, `now` as price,
             `volume`, `hold`
             from ''' + where + ''' order by time_index;'''
    df = pd.read_sql(sql, pandas_yhdb)
    return df


def main(ifcode, period_short, period_long):
    rs = []
    total = 0
    pos_num = 0
    nag_num = 0
    date_list = ifcode_day_map(ifcode)
    for day in date_list:
        df = get_data(ifcode, day)
        #df = point_prosess_v2(_df, 30)
        df['ema_short'] = Indicator.ewma_metric(period_short, df[['price']], 'price')
        df['ema_long'] = Indicator.ewma_metric(period_long, df[['price']], 'price')

        sig_infos = SellSignal.compare_ema(df, period_short, offset=5)
        profit_infos = SellSignal.profit_infos(sig_infos)
        profit_all = 0
        trans_num = (len(profit_infos) + 1) / 2
        for item in profit_infos:
            if item['gain'] != '-':
                profit_all += int(item['gain'])
        rs.append({day: profit_all, 'trans_num': trans_num})
        total += profit_all
        if profit_all >= 0:
            pos_num += 1
        elif profit_all < 0 :
            nag_num += 1

    pprint(rs)
    print '%s total: %s' % (ifcode, total)
    print '%s profit rate: %.2f' % (ifcode, pos_num*1.0/nag_num)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="save ema dataframe to files")
    parser.add_argument("ifcode", type=str, help="ifcode")
    parser.add_argument("period_short", type=int, help="short period")
    parser.add_argument("period_long", type=int, help="long period")
    args = parser.parse_args()
    ifcode = args.ifcode
    period_short = args.period_short
    period_long = args.period_long
    main(ifcode, period_short, period_long)
