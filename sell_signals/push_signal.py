# -*- coding: utf8 -*-

from datetime import datetime, date


class PushSellSignal(object):

    @classmethod
    def compare_sig(cls, df, short_name, long_name, offset=1000, trans_num=4):
        today = date.today()
        year, month, day = today.year, today.month, today.day

        time_index = list(df['time_index'])
        price = list(df['price'])
        sig_short = list(df[short_name])
        sig_long = list(df[long_name])
        price_num = len(price)
        signal_infos = []
        diff_list = [(sig_short[i] - sig_long[i]) for i in range(price_num)]
        for i in range(price_num):
            if i >= offset:
                _s = diff_list[i-1]
                _sa = diff_list[i]
                if (_s * _sa) <= 0:
                    t = {}
                    if _s > 0 and _sa <= 0:
                        t['event'] = '卖出信号'
                    elif _s < 0 and _sa >= 0:
                        t['event'] = '买入信号'
                    else:
                        continue
                    t['index'] = time_index[i]
                    t['price'] = price[i]
                    t['gain'] = '-' #盈利
                    t['info'] = ''
                    signal_infos.append(t)
                if (len(signal_infos)) >= trans_num: #控制交易次数
                    t = {}
                    t['event'] = '收盘平仓'
                    t['index'] = time_index[i]
                    t['price'] = price[i]
                    t['gain'] = '-'
                    t['info'] = '收盘前平仓'
                    signal_infos.append(t)
                    break
            if datetime.now() > datetime(year, month, day, 14, 58, 00) and i>= price_num - 1:
                # 时间条件是控制实时信号
                t = {}
                t['event'] = '收盘平仓'
                t['index'] = time_index[i]
                t['price'] = price[i]
                t['gain'] = '-'
                t['info'] = '收盘前平仓'
                signal_infos.append(t)
                break

        return signal_infos

    @classmethod
    def compare_ema(cls, ema_df, offset=1000):
        today = date.today()
        year, month, day = today.year, today.month, today.day

        time_index = list(ema_df['time_index'])
        price = list(ema_df['price'])
        ema_short = list(ema_df['ema_short'])
        ema_long = list(ema_df['ema_long'])
        price_num = len(price)
        signal_infos = []
        diff_list = [(ema_short[i] - ema_long[i]) for i in range(price_num)]
        for i in range(price_num):
            if i >= offset:
                _s = diff_list[i-1]
                _sa = diff_list[i]
                if (_s * _sa) <= 0:
                    t = {}
                    if _s > 0 and _sa <= 0:
                        t['event'] = '卖出信号'
                    elif _s < 0 and _sa >= 0:
                        t['event'] = '买入信号'
                    else:
                        continue
                    t['index'] = time_index[i]
                    t['price'] = price[i]
                    t['gain'] = '-' #盈利
                    t['info'] = ''
                    signal_infos.append(t)
            if datetime.now() > datetime(year, month, day, 14, 56, 00) and i > price_num - 10:
                # 时间条件是控制实时信号
                t = {}
                t['event'] = '收盘平仓'
                t['index'] = time_index[i]
                t['price'] = price[i]
                t['gain'] = '-'
                t['info'] = '收盘前平仓'
                signal_infos.append(t)
                break

        return signal_infos

    @classmethod
    def profit_infos(cls, signal_infos):
        info = []
        for i in range(len(signal_infos)):
            diff_price = 0
            if i > 0 and i < len(signal_infos):
                now_p = signal_infos[i]['price']
                befo_p = signal_infos[i-1]['price']
                diff_price = (now_p - befo_p) * 300
                del signal_infos[i-1]['index']
                info.append(signal_infos[i-1])
                t = {}
                if signal_infos[i-1]['event'] == '买入信号' and diff_price >= 0:
                    t['event'] = '平仓盈利'
                    t['price'] = '-'
                    t['gain'] = diff_price
                    t['info'] = '盈利, 在 %.2f 点进行平仓' % now_p
                    info.append(t)
                elif signal_infos[i-1]['event'] == '买入信号' and diff_price <= 0:
                    t['event'] = '平仓亏损'
                    t['price'] = '-'
                    t['gain'] = diff_price
                    t['info'] = '亏损, 在 %.2f 点进行平仓' % now_p
                    info.append(t)
                elif signal_infos[i-1]['event'] == '卖出信号' and diff_price >= 0:
                    t['event'] = '平仓亏损'
                    t['price'] = '-'
                    t['gain'] = diff_price * (-1)
                    t['info'] = '亏损, 在 %.2f 点进行平仓' % now_p
                    info.append(t)
                elif signal_infos[i-1]['event'] == '卖出信号' and diff_price <= 0:
                    t['event'] = '平仓盈利'
                    t['price'] = '-'
                    t['gain'] = diff_price * (-1)
                    t['info'] = '盈利, 在 %.2f 点进行平仓' % now_p
                    info.append(t)
            if i == len(signal_infos) - 1:
                del signal_infos[i]['index']
                info.append(signal_infos[i])
        return info
