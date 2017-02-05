# -*- coding: utf8 -*-

import pandas as pd

def ma(n, series):
    return sum(series) / n*1.0


def ema(n, series):
    y = 0
    for i in range(n):
        y = (2.0 * series[i] + (i+1-1) * y) / ((i+1)+1) * 1.0
    return y


def boll_md(n, series, ma_list):
    md = 0
    _sum = 0
    for i in range(n):
        _sum += (series[i] - ma_list[i])**2
        md = (_sum / n*1.0)**(0.5)
    return md


class Indicator(object):

    @classmethod
    def ema_metric(cls, n, series):
        ema_mt = []
        for i in range(len(series)):
            if i >= n-1:
                _ema = ema(n, series[i-n+1: i+1])
                ema_mt.append(_ema)
            elif i <= 1:
                ema_mt.append(series[0])
            else:
                _ema = ema(i, series[: i+1])
                ema_mt.append(_ema)
        return ema_mt

    @classmethod
    def ma_metric(cls, n, series):
        ma_mt = []
        for i in range(len(series)):
            if i >= n-1:
                _ma = ma(n, series[i-n+1: i+1])
                ma_mt.append(_ma)
            else:
                ma_mt.append(series[0])
        return ma_mt


    @classmethod
    def ma_metric_v2(cls, n, df_price, name):
        ma_df = pd.rolling_median(df_price[[name]], n)
        ma_mt = list(ma_df[name])
        return ma_mt


    @classmethod
    def ewma_metric(cls, n, df_price, name, adjust=True):
        ewma_df = pd.ewma(df_price[[name]], n, adjust=adjust)
        ewma_mt = list(ewma_df[name])
        return ewma_mt

    @classmethod
    def boll_md_metric(cls, n, series):
        ma_list = cls.ma_metric(n, series)
        boll_md_mt = []
        for i in range(len(series)):
            if i >= n-1:
                _boll_nd = boll_md(n, series[i-n+1: i+1], ma_list[i-n+1: i+1])
                boll_md_mt.append(_boll_nd)
            else:
                boll_md_mt.append(0)
        return boll_md_mt


def point_prosess(df, offset=40):
    data_list = df[['time_index', 'price']].values.tolist()
    rs = []
    for i in range(len(df)):
        if i%offset == 0:
            rs.append(data_list[i])
    _df = pd.DataFrame(rs, columns=['time_index', 'price'])
    return _df


def point_prosess_v2(df, offset=20):
    data_list = df[['time_index', 'price']].values.tolist()
    rs = []
    for i in range(len(df)):
        if i%offset == 0:
            if i == 0:
                rs.append(data_list[i])
            else:
                _time_index = data_list[i][0]
                _p_list = [item[1] for item in data_list[i-offset: i]]
                _df = pd.DataFrame(_p_list)
                #_p = _df.mean()[0]
                _p = _df.median()[0]
                rs.append([_time_index, _p])
    _df = pd.DataFrame(rs, columns=['time_index', 'price'])
    return _df


def point_prosess_v3(df, offset=8):
    _df = point_prosess_v2(df, offset)
    _dff = point_prosess_v2(_df, offset)
    '''
    import pprint
    pprint.pprint(_dff)
    '''
    #print len(_dff)
    return _dff


