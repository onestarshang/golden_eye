# -*- coding: utf8 -*-

import sys, os
from os.path import dirname
sys.path.insert(0, dirname(dirname(os.path.abspath(__file__))))
import argparse
from simplejson import dumps
from datetime import date

from models.api.backtest.calculator import FittingDataCalculator

save_dir = '/root/ema_backtest_data'

def save_data(df, date, ifcode, period_short, period_long):
    f = open('%s/%s_%s_%s_%s' % (save_dir, date, ifcode, period_short, period_long), 'w')
    try:
        f.write(dumps(df))
        f.close()
    except BaseException, e:
        print e
        f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="save ema dataframe to files")
    parser.add_argument("ifcode", type=str, help="ifcode")
    parser.add_argument("period_short", type=int, help="short period")
    parser.add_argument("period_long", type=int, help="long period")
    args = parser.parse_args()
    ifcode = args.ifcode
    period_short = args.period_short
    period_long = args.period_long
    thedate = date.today().strftime('%Y-%m-%d')

    df = FittingDataCalculator.ema_df(thedate, ifcode, period_short, period_long)
    save_data(df.values.tolist(), thedate, ifcode, period_short, period_long)
