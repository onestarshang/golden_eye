# -*- coding: utf8 -*-

import sys, os
from os.path import dirname
sys.path.insert(0, dirname(dirname(os.path.abspath(__file__))))
import argparse
import simplejson
from pprint import pprint

from consts import macd_param_analysis_dir, init_point, init_time, init_offset
from models.api.backtest.analysis import DataAnalyzer


def conbine_sig(ema_signals, macd_signals):
    pprint(ema_signals)
    print '********************************'
    pprint(macd_signals)
    pass


def main(ifcode, date):
    '''
    ema_signals = DataAnalyzer.ema(date, ifcode, 480, 1400)
    macd_signals = DataAnalyzer.macd(date, ifcode, period_short=12, period_long=26, period_dif=9, \
             pre_point=init_point, pre_time=init_time, offset=init_offset)
    conbine_sig(ema_signals, macd_signals)
    '''
    boll_sig = DataAnalyzer.boll(date, ifcode)
    print len(boll_sig)
    for item in boll_sig:
        print item['event']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="macd metric params maker")
    parser.add_argument("ifcode", type=str, help="ifcode")
    parser.add_argument("date", type=str, help="date like: 2016-01-04")
    args = parser.parse_args()
    ifcode = args.ifcode
    thedate = args.date
    main(ifcode, thedate)
