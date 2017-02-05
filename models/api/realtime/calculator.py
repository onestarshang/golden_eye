# -*- coding:utf8 -*-

import pandas as pd
import os
from datetime import datetime

from indicator import Indicator, point_prosess
from yhapi.mongodb_mod import yh_mongodb

from libs.utils import day2int

column_key = ['InsertTime', 'Time', 'Now', 'Open',\
              'High', 'Low', 'CurHold', 'Hold',\
              'Volume', 'BuyVolume', 'SellVolume', 'VolumeRate']


def realtime_data(today, ifcode):
    coll_name = '%s_data_second' % ifcode
    coll = yh_mongodb[coll_name]

    year, month, day = today.year, today.month, today.day
    datetime_s1 = datetime(year, month, day, 9, 30, 00)
    datetime_e1 = datetime(year, month, day, 11, 30, 00)
    datetime_s2 = datetime(year, month, day, 13, 00, 00)
    datetime_e2 = datetime(year, month, day, 15, 00, 00)
    rows = coll.find({"$or": [{"InsertTime": {"$gte": datetime_s1, '$lt': datetime_e1}},
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
            _t = [day2int(tmp[1]), tmp[2], tmp[8]]
            rs.append(_t)
    return rs


class BollCalculator(object):

    @classmethod
    def boll_chart(cls, date, ifcode, period_short=50, period_long=80, offset=10):
        df_list = realtime_data(date, ifcode)
        df = pd.DataFrame(df_list, columns=['time_index', 'price', 'volume'])
        boll_df = point_prosess(df, offset)
        price_list = list(boll_df['price'])
        boll_df['boll_mb'] = Indicator.ma_metric(period_short, price_list)
        mb_list = list(boll_df['boll_mb'])
        boll_df['boll_md'] = Indicator.boll_md_metric(period_long, mb_list)
        boll_df['boll_up'] = boll_df['boll_mb'] + 2.0*boll_df['boll_md']
        boll_df['boll_dn'] = boll_df['boll_mb'] - 2.0*boll_df['boll_md']

        price = boll_df[['time_index', 'price']].values.tolist()
        boll_up = boll_df[['time_index', 'boll_up']].values.tolist()
        boll_dn = boll_df[['time_index', 'boll_dn']].values.tolist()
        boll_mb = boll_df[['time_index', 'boll_mb']].values.tolist()
        return price, boll_up, boll_dn, boll_mb
