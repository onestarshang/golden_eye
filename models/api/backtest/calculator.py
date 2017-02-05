# -*- coding: utf8 -*-

import pandas as pd
import os
from simplejson import loads

from models.api.backtest.tables import BacktestData
from indicator import Indicator, point_prosess, point_prosess_v2, point_prosess_v3
from consts import ema_file_dir


def read_df(path):
    df_list = loads(open(path).read())
    return pd.DataFrame(df_list, columns=['time_index', 'price', 'volume',
                                          'ema_short', 'ema_long'])


class FittingDataCalculator(object):

    @classmethod
    def raw_series(cls, date, ifcode):
        data = BacktestData.get_data_by_ifcode(date, ifcode)
        df = pd.DataFrame(data, columns=['time_index', 'price', 'volume'])
        price = df[['time_index', 'price']].values.tolist()
        volume = df[['time_index', 'volume']].values.tolist()
        return [price, volume]

    @classmethod
    def fitting_series(cls, period, date, ifcode):
        data = BacktestData.get_data_by_ifcode(date, ifcode)
        df = pd.DataFrame(data, columns=['time_index', 'price', 'volume'])
        return df[['time_index', 'price']].values.tolist()

    @classmethod
    def ema_chart(cls, date, ifcode, period_short, period_long):
        _file = '%s/%s_%s_%s_%s' % (ema_file_dir, date, ifcode, period_short, period_long)
        if os.path.isfile(_file):
            df = read_df(_file)
        else:
            data = BacktestData.get_data_by_ifcode(date, ifcode)
            df = pd.DataFrame(data, columns=['time_index', 'price', 'volume'])
            price = list(df['price'])
            df['ema_short'] = Indicator.ema_metric(period_short, price)
            df['ema_long'] = Indicator.ema_metric(period_long, price)
        price = df[['time_index', 'price']].values.tolist()
        ema_short = df[['time_index', 'ema_short']].values.tolist()
        ema_long = df[['time_index', 'ema_long']].values.tolist()
        volume = df[['time_index', 'volume']].values.tolist()
        return [price, ema_short, ema_long, volume]

    @classmethod
    def ema_df(cls, date, ifcode, period_short, period_long):
        data = BacktestData.get_data_by_ifcode(date, ifcode)
        if not data:
            return pd.DataFrame()
        df = pd.DataFrame(data, columns=['time_index', 'price', 'volume'])
        price = list(df['price'])
        df['ema_short'] = Indicator.ema_metric(period_short, price)
        df['ema_long'] = Indicator.ema_metric(period_long, price)
        return df

    @classmethod
    def boll_df(cls, date, ifcode, period_short, period_long, pre_point):
        data = BacktestData.get_data_by_ifcode(date, ifcode)
        if not data:
            return pd.DataFrame()
        _df = pd.DataFrame(data, columns=['time_index', 'price', 'volume'])
        df = point_prosess(_df, pre_point)
        price_list = list(df['price'])
        df['boll_mb'] = Indicator.ma_metric(period_short, price_list)
        mb_list = list(df['boll_mb'])
        df['boll_md'] = Indicator.boll_md_metric(period_long, mb_list)
        df['boll_up'] = df['boll_mb'] + 2.0*df['boll_md']
        df['boll_dn'] = df['boll_mb'] - 2.0*df['boll_md']

        return df


    #******************************************************************************************
    #macd
    @classmethod
    def macd_df(cls, date, ifcode, period_short, period_long, period_dif, pre_point, pre_time):
        data = BacktestData.get_macd_data_by_ifcode(date, ifcode, pre_time)
        if not data:
            return pd.DataFrame()
        _df = pd.DataFrame(data, columns=['time_index', 'price', 'volume'])
        df = point_prosess_v3(_df, pre_point)
        #df = point_prosess_v2(_df, pre_point)
        df['ma_short'] = Indicator.ewma_metric(period_short, df[['price']], 'price', False)
        df['ma_long'] = Indicator.ewma_metric(period_long, df[['price']], 'price', False)
        df['macd_dif'] = df['ma_short'] - df['ma_long']
        df['macd_dem'] = Indicator.ewma_metric(period_dif, df[['macd_dif']], 'macd_dif', True)
        return df
