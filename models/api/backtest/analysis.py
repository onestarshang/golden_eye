# -*- coding: utf8 -*-

import os
from simplejson import loads
import pandas as pd

from models.api.backtest.calculator import FittingDataCalculator
from sell_signals.base import SellSignal
from consts import ema_file_dir, init_point, init_time, init_offset
from libs.utils import ifcode_day_map

def read_df(path):
    df_list = loads(open(path).read())
    return pd.DataFrame(df_list, columns=['time_index', 'price', 'volume',
                                          'ema_short', 'ema_long'])


class DataAnalyzer(object):

    @classmethod
    def ema(cls, date, ifcode, period_short, period_long):
        _file = '%s/%s_%s_%s_%s' % (ema_file_dir, date, ifcode, period_short, period_long)
        if os.path.isfile(_file):
            df = read_df(_file)
        else:
            df = FittingDataCalculator.ema_df(date, ifcode, period_short, period_long)
            if df.empty:
                return []
        sig_infos = SellSignal.compare_ema(df, limit_period=60)
        profit_infos = SellSignal.profit_infos(sig_infos)
        return profit_infos

    #**************************************************************
    #macd
    @classmethod
    def macd(cls, date, ifcode, period_short=12, period_long=26, period_dif=9, \
             pre_point=init_point, pre_time=init_time, offset=init_offset):
        #date : 'yyyy-mm-dd'
        df = FittingDataCalculator.macd_df(date, ifcode, period_short, period_long, \
                                           period_dif, pre_point, pre_time)
        if df.empty:
            return []
        sig_infos = SellSignal.compare_macd(df, 3, offset)
        profit_infos = SellSignal.profit_infos(sig_infos)
        flags = SellSignal.out_flags(sig_infos)
        return profit_infos

    @classmethod
    def macd_chart(cls, date, ifcode, period_short=12, period_long=26, period_dif=9, \
                   pre_point=init_point, pre_time=init_time, offset=init_offset):
        df = FittingDataCalculator.macd_df(date, ifcode, period_short, period_long, \
                                           period_dif, pre_point, pre_time)

        price = df[['time_index', 'price']].values.tolist()
        macd_dif = df[['time_index', 'macd_dif']].values.tolist()
        macd_dem = df[['time_index', 'macd_dem']].values.tolist()

        # flag
        sig_infos = SellSignal.compare_macd(df, 3, offset)
        flags = SellSignal.out_flags(sig_infos)
        return [price, macd_dif, macd_dem, flags]


    #*********************************************************
    #analysis
    #*********************************************************
    @classmethod
    def macd_analysis(cls, date, ifcode, period_short, period_long, \
                      period_dif, pre_point, pre_time, pre_offset):
        #date : 'yyyy-mm-dd'
        df = FittingDataCalculator.macd_df(date, ifcode, period_short, period_long, \
                                        period_dif, pre_point, pre_time)
        if df.empty:
            return []
        sig_infos = SellSignal.compare_macd(df, 3, pre_offset)
        profit_infos = SellSignal.profit_infos(sig_infos)
        return profit_infos


    @classmethod
    def macd_if_analysis(cls, ifcode, pre_point, pre_time, pre_offset, \
                         period_short=12, period_long=26, period_dif=9, trans_amount=1):
        rs = []
        total = 0
        pos_num = 0
        nag_num = 0
        trans_total_num = 0
        date_list = ifcode_day_map(ifcode)
        for day in date_list:
            profit_infos = cls.macd_analysis(day, ifcode, period_short, period_long, \
                                             period_dif, pre_point, pre_time, pre_offset)
            profit_all = 0
            trans_num = (len(profit_infos) - 1) / 2
            trans_total_num += trans_num
            for item in profit_infos:
                if item['gain'] != '-':
                    profit_all += int(item['gain']) * trans_amount
            rs.append({'date': day, 'profit': profit_all, 'trans_num': trans_num})
            total += profit_all
            if profit_all >= 0:
                pos_num += 1
            elif profit_all < 0 :
                nag_num += 1

        if nag_num == 0:
            profit_rate = pos_num
        else:
            profit_rate = pos_num*1.0/nag_num
        fees = trans_total_num * 2300
        real_profit = total - fees
        return {'profit': total, 'real_profit': real_profit,
                'profit_rate': profit_rate, 'trans_total_num': trans_total_num,
                'fees': fees, 'trans_amount': trans_amount}



    #*************************************************************
    #boll
    @classmethod
    def boll_chart(cls, date, ifcode, period_short=50, period_long=80, pre_point=10):
        df = FittingDataCalculator.boll_df(date, ifcode, period_short, period_long, pre_point)

        price = df[['time_index', 'price']].values.tolist()
        boll_up = df[['time_index', 'boll_up']].values.tolist()
        boll_dn = df[['time_index', 'boll_dn']].values.tolist()
        boll_mb = df[['time_index', 'boll_mb']].values.tolist()
        return price, boll_up, boll_dn, boll_mb

    @classmethod
    def boll(cls, date, ifcode, period_short=50, period_long=80, pre_point=10):
        df = FittingDataCalculator.boll_df(date, ifcode, period_short, period_long, pre_point)
        sig_infos = SellSignal.compare_boll_b_percent(df)
        profit_infos = SellSignal.profit_infos(sig_infos)
        return profit_infos


