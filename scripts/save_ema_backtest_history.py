# -*- coding: utf8 -*-

import sys, os
from os.path import dirname
sys.path.insert(0, dirname(dirname(os.path.abspath(__file__))))
import argparse
from simplejson import dumps

from models.api.backtest.calculator import FittingDataCalculator
from libs.mysql_mod import yhdb

save_dir = '/root/ema_backtest_data'

def save_data(df, date, ifcode, period_short, period_long):
    f = open('%s/%s_%s_%s_%s' % (save_dir, date, ifcode, period_short, period_long), 'w')
    try:
        f.write(dumps(df))
        f.close()
    except BaseException, e:
        print e
        f.close()


def ifcode_day_map(ifcode):
    sql = '''select distinct date(`time`) from %s;''' % ifcode
    rs = yhdb(sql)
    return [d[0].strftime('%Y-%m-%d') for d in rs]


def main(ifcode, period_short, period_long):
    date_list = ifcode_day_map(ifcode)
    for day in date_list:
        print '*'*20
        print day
        df = FittingDataCalculator.ema_df(day, ifcode, period_short, period_long)
        save_data(df.values.tolist(), day, ifcode, period_short, period_long)


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
