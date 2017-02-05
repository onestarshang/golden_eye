#-*- coding: utf8 -*-

import sys, os
from os.path import dirname
sys.path.insert(0, dirname(dirname(os.path.abspath(__file__))))

import time
import traceback
from datetime import datetime, timedelta, date
import pandas as pd
import simplejson

from pushover import init, Client

from yhapi.utils import UTC_time, ifcode_map
from yhapi.mongodb_mod import yh_mongodb

from sell_signals.push_signal import PushSellSignal
from indicator import Indicator, point_prosess_v2, point_prosess_v3
from consts import old_infos_dir, validate_df_dir
from libs.utils import str2day, pre_day

column_key = ['InsertTime', 'Time', 'Now', 'Open',\
              'High', 'Low', 'CurHold', 'Hold',\
              'Volume', 'BuyVolume', 'SellVolume', 'VolumeRate']


def realtime_data(ifcode, code, today):
    coll_name = '%s_data_second' % ifcode.lower()
    coll = yh_mongodb[coll_name]

    pre = pre_day(today)
    _pre_year, _pre_month, _pre_day = pre.year, pre.month, pre.day
    pre_datetime_s1 = datetime(_pre_year, _pre_month, _pre_day, 14, 34, 00)
    pre_datetime_e1 = datetime(_pre_year, _pre_month, _pre_day, 15, 00, 00)

    year, month, day = today.year, today.month, today.day
    datetime_s1 = datetime(year, month, day, 9, 15, 00)
    datetime_e1 = datetime(year, month, day, 11, 30, 00)
    datetime_s2 = datetime(year, month, day, 13, 00, 00)
    datetime_e2 = datetime(year, month, day, 15, 15, 00)
    rows = coll.find({"$or": [{"InsertTime": {"$gte": pre_datetime_s1, '$lt': pre_datetime_e1}},
                              {"InsertTime": {"$gte": datetime_s1, '$lt': datetime_e1}},
                              {"InsertTime": {"$gte": datetime_s2, '$lt': datetime_e2}}]},\
                     {'_id': -1, 'InsertTime': 1, 'Time': 1, 'Now': 1,\
                      'High': 1, 'Open': 1, 'CurHold': 1, 'Hold': 1, 'Low': 1,\
                      'Volume': 1, 'BuyVolume': 1, 'SellVolume': 1, 'VolumeRate':1}).sort('InsertTime')
    rs = []
    for doc in rows:
        tmp = []
        for k in column_key:
            if k in doc:
                tmp.append(doc[k])
        if len(tmp) == 12:
            _t = [tmp[1], tmp[2], tmp[8]]
            rs.append(_t)
    return rs


def save_df(df_list, ifcode, today, period_short, period_long):
    df = pd.DataFrame(df_list, columns=['time_index', 'price', 'volume'])
    price = list(df['price'])
    df['ema_short'] = Indicator.ema_metric(period_short, price)
    df['ema_long'] = Indicator.ema_metric(period_long, price)

    #macd
    macd_df = point_prosess_v3(df, 8)
    macd_df['ma_short'] = Indicator.ewma_metric(12, macd_df[['price']], 'price', False)
    macd_df['ma_long'] = Indicator.ewma_metric(26, macd_df[['price']], 'price', False)
    macd_df['macd_dif'] = macd_df['ma_short'] - macd_df['ma_long']
    macd_dif = list(macd_df['macd_dif'])
    macd_df['macd_dem'] = Indicator.ewma_metric(9, macd_df[['macd_dif']], 'macd_dif')

    _macd_file = '%s/%s_%s_macd' % (validate_df_dir, ifcode, today)
    macd_df.to_csv(_macd_file, index=False)

    sig_infos = PushSellSignal.compare_sig(macd_df, 'macd_dif', 'macd_dem', 16)
    profit_infos = PushSellSignal.profit_infos(sig_infos)
    print '*******macd******'
    print profit_infos
    print len(profit_infos)

    _file = '%s/%s_%s' % (validate_df_dir, ifcode, today)
    df.to_csv(_file, index=False)

    sig_infos = PushSellSignal.compare_sig(df, 'ema_short', 'ema_long')
    profit_infos = PushSellSignal.profit_infos(sig_infos)
    print '*******ema*******'
    print profit_infos
    print len(profit_infos)


def main(ifcode, code, period_short, period_long):
    today = date.today()
    df_list = realtime_data(ifcode, code, today)
    print len(df_list)
    save_df(df_list, ifcode, today, period_short, period_long)


if __name__ == '__main__':
    arg = sys.argv
    ifcode, code, period_short, period_long = arg[1:]
    #ifcode, code = 'IF1509', '040109'
    main(ifcode, code, int(period_short), int(period_long))
