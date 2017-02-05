# -*- coding: utf8 -*-


class SellSignal(object):

    @classmethod
    def out_flags(cls, signal_infos):
        flags = []
        for info in signal_infos:
            if info['index'] != -1:
                if '卖' in info['event']:
                    flags.append([info['index'], '卖', info['price']])
                elif '买' in info['event']:
                    flags.append([info['index'], '买', info['price']])
        return flags

    @classmethod
    def compare_macd_old(cls, macd_df, limit_period=11, offset=30):
        time_index = list(macd_df['time_index'])
        price = list(macd_df['price'])
        macd_dif = list(macd_df['macd_dif'])
        macd_dem = list(macd_df['macd_dem'])
        price_num = len(price)
        signal_infos = []
        diff_list = [(macd_dif[i] - macd_dem[i]) for i in range(price_num)]
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
            if i > price_num - limit_period:
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
    def compare_macd(cls, macd_df, limit_period=11, offset=30, trans_num=4, init_offset=5):
        time_index = list(macd_df['time_index'])
        price = list(macd_df['price'])
        macd_dif = list(macd_df['macd_dif'])
        macd_dem = list(macd_df['macd_dem'])
        price_num = len(price)
        signal_infos = []
        diff_list = [(macd_dif[i] - macd_dem[i]) for i in range(price_num)]
        for i in range(price_num):
            '''
            if i == 8:
                t = {}
                if diff_list[i] > 0 :
                    t['event'] = '买入信号'
                else:
                    t['event'] = '卖出信号'
                t['index'] = time_index[i]
                t['price'] = price[i]
                t['gain'] = '-' #盈利
                t['info'] = ''
                signal_infos.append(t)
            '''
            if i >= offset:
                _s = diff_list[i-1]
                _sa = diff_list[i]
                if (_s * _sa) <= 0:
                    t = {}
                    if _s > 0 and _sa <= 0:
                        '''
                        if (len(signal_infos) == 1 and signal_infos[0]['event'] != '卖出信号') \
                                or len(signal_infos) > 1:
                            t['event'] = '卖出信号'
                        else:
                            continue
                        '''
                        t['event'] = '卖出信号'
                    elif _s < 0 and _sa >= 0:
                        '''
                        if (len(signal_infos) == 1 and signal_infos[0]['event'] != '买入信号') \
                                or len(signal_infos) > 1:
                            t['event'] = '买入信号'
                        else:
                            continue
                        '''
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

            if i > price_num - limit_period:
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
    def compare_ema(cls, ema_df, limit_period=1000, offset=1000):
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
            if i > price_num - limit_period:
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
    def compare_boll(cls, boll_df, limit_period=2, offset=52):
        time_index = list(boll_df['time_index'])
        price = list(boll_df['price'])
        boll_dn = list(boll_df['boll_dn'])
        boll_up = list(boll_df['boll_up'])
        boll_mb = list(boll_df['boll_mb'])
        price_num = len(price)
        signal_infos = []
        up_diff_list = [(price[i] - boll_up[i]) for i in range(price_num)]
        dn_diff_list = [(price[i] - boll_dn[i]) for i in range(price_num)]
        mb_diff_list = [(price[i] - boll_mb[i]) for i in range(price_num)]

        for i in range(price_num):
            if i == offset:
                #初始化趋势信号, price compare mid line
                positive_num = len([item for item in mb_diff_list[:i] if item>0])
                negative_num = len([item for item in mb_diff_list[:i] if item<0])
                pos_req = positive_num * 1.0 / i
                neg_req = negative_num * 1.0 / i
                if pos_req >= 0.8:
                    t = {}
                    t['event'] = '上涨趋势'
                    t['index'] = time_index[i]
                    t['price'] = price[i]
                    t['gain'] = '-' #盈利
                    t['info'] = ''
                elif neg_req >= 0.8:
                    t = {}
                    t['event'] = '下跌趋势'
                    t['index'] = time_index[i]
                    t['price'] = price[i]
                    t['gain'] = '-' #盈利
                    t['info'] = ''
                else:
                    t = {}
                    t['event'] = '可能横盘'
                    t['index'] = time_index[i]
                    t['price'] = price[i]
                    t['gain'] = '-' #盈利
                    t['info'] = ''
                signal_infos.append(t)
            elif i > offset:
                # price up sig
                up_s = up_diff_list[i-1]
                up_sa = up_diff_list[i]

                # price dn sig
                dn_s = dn_diff_list[i-1]
                dn_sa = dn_diff_list[i]

                # price mb sig
                mb_s = mb_diff_list[i-1]
                mb_sa = mb_diff_list[i]
                if (up_s * up_sa) <= 0:
                    t = {}
                    if up_s > 0 and up_sa <= 0:
                        t['event'] = '价格向下穿越上线'
                        t['index'] = time_index[i]
                        t['price'] = price[i]
                        t['gain'] = '-' #盈利
                        t['info'] = ''
                        signal_infos.append(t)
                    elif up_s < 0 and up_sa >= 0:
                        t['event'] = '价格向上穿越上线'
                        t['index'] = time_index[i]
                        t['price'] = price[i]
                        t['gain'] = '-' #盈利
                        t['info'] = ''
                        signal_infos.append(t)
                elif (dn_s * dn_sa) <= 0:
                    t = {}
                    if dn_s > 0 and dn_sa <= 0:
                        t['event'] = '价格向下穿越下线'
                        t['index'] = time_index[i]
                        t['price'] = price[i]
                        t['gain'] = '-' #盈利
                        t['info'] = ''
                        signal_infos.append(t)
                    elif dn_s < 0 and dn_sa >= 0:
                        t['event'] = '价格向上穿越下线'
                        t['index'] = time_index[i]
                        t['price'] = price[i]
                        t['gain'] = '-' #盈利
                        t['info'] = ''
                        signal_infos.append(t)
                elif (mb_s * mb_sa) <= 0:
                    t = {}
                    if mb_s > 0 and mb_sa <= 0:
                        t['event'] = '价格向下穿越中线'
                        t['index'] = time_index[i]
                        t['price'] = price[i]
                        t['gain'] = '-' #盈利
                        t['info'] = ''
                        signal_infos.append(t)
                    elif mb_s < 0 and mb_sa >= 0:
                        t['event'] = '价格向上穿越中线'
                        t['index'] = time_index[i]
                        t['price'] = price[i]
                        t['gain'] = '-' #盈利
                        t['info'] = ''
                        signal_infos.append(t)
            elif i > price_num - limit_period:
                t = {}
                t['event'] = '收盘平仓'
                t['index'] = time_index[i]
                t['price'] = price[i]
                t['gain'] = '-'
                t['info'] = '收盘前平仓'
                signal_infos.append(t)
                break

        return cls.boll_merge_sig(signal_infos, limit_period)
        #return signal_infos

    @classmethod
    def compare_boll_b_percent(cls, boll_df, limit_period=2, offset=52, trans_num=100):
        time_index = list(boll_df['time_index'])
        price = list(boll_df['price'])
        boll_dn = list(boll_df['boll_dn'])
        boll_up = list(boll_df['boll_up'])
        boll_mb = list(boll_df['boll_mb'])
        price_num = len(price)
        signal_infos = []
        dn_diff_list = [(price[i] - boll_dn[i]) for i in range(price_num)]
        up_dn_diff_list = [(boll_up[i] - boll_dn[i]) for i in range(price_num)]

        diff_list = []
        for i in range(price_num):
            _b = dn_diff_list[i] * 1.0 / up_dn_diff_list[i]
            diff_list.append(_b)
        #print diff_list
        for i in range(price_num):
            if i >= offset:
                t = {}
                if diff_list[i] < 0:
                    t['event'] = '卖出信号'
                    t['index'] = time_index[i]
                    t['price'] = price[i]
                    t['gain'] = '-' #盈利
                    t['info'] = ''
                    signal_infos.append(t)
                elif diff_list[i] > 1:
                    t['event'] = '买入信号'
                    t['index'] = time_index[i]
                    t['price'] = price[i]
                    t['gain'] = '-' #盈利
                    t['info'] = ''
                    signal_infos.append(t)
                else:
                    continue

                if (len(signal_infos)) >= trans_num: #控制交易次数
                    t = {}
                    t['event'] = '收盘平仓'
                    t['index'] = time_index[i]
                    t['price'] = price[i]
                    t['gain'] = '-'
                    t['info'] = '收盘前平仓'
                    signal_infos.append(t)
                    break

            if i > price_num - limit_period:
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
    def boll_merge_sig(cls, signal_infos, limit_period):
        '''
        for item in signal_infos:
            print item['event']
        '''
        new_sig_infos = []
        for i in range(len(signal_infos)):
            if i == 0:
                if signal_infos[i]['event'] == '上涨趋势':
                    t = {}
                    t = signal_infos[i]
                    t['event'] = '买入信号'
                    new_sig_infos.append(t)
                elif signal_infos[i]['event'] == '下跌趋势':
                    t = {}
                    t = signal_infos[i]
                    t['event'] = '买入信号'
                    new_sig_infos.append(t)
            if i >= 2 and i < len(signal_infos):
                if signal_infos[i-2]['event'] == '价格向下穿越下线' \
                        and signal_infos[i-1]['event'] == '价格向上穿越下线' \
                        and signal_infos[i]['event'] == '价格向上穿越中线':
                    t = {}
                    t = signal_infos[i]
                    t['event'] = '买入信号'
                    new_sig_infos.append(t)
                if signal_infos[i-2]['event'] == '价格向上穿越上线' \
                        and signal_infos[i-1]['event'] == '价格向下穿越上线' \
                        and signal_infos[i]['event'] == '价格向下穿越中线':
                    t = {}
                    t = signal_infos[i]
                    t['event'] = '卖出信号'
                    new_sig_infos.append(t)
                if signal_infos[i]['event'] == '收盘平仓':
                    new_sig_infos.append(signal_infos[i])
        return new_sig_infos


    @classmethod
    def profit_infos(cls, signal_infos):
        info = []
        for i in range(len(signal_infos)):
            diff_price = 0
            if i > 0 and i < len(signal_infos):
                now_p = signal_infos[i]['price']
                befo_p = signal_infos[i-1]['price']
                diff_price = (now_p - befo_p) * 300
                info.append(signal_infos[i-1])
                t = {}
                if signal_infos[i-1]['event'] == '买入信号' and diff_price >= 0:
                    t['event'] = '平仓盈利'
                    t['index'] = -1
                    t['price'] = '-'
                    t['gain'] = diff_price
                    t['info'] = '盈利, 在 %.2f 点进行平仓' % now_p
                    info.append(t)
                elif signal_infos[i-1]['event'] == '买入信号' and diff_price <= 0:
                    t['event'] = '平仓亏损'
                    t['index'] = -1
                    t['price'] = '-'
                    t['gain'] = diff_price
                    t['info'] = '亏损, 在 %.2f 点进行平仓' % now_p
                    info.append(t)
                elif signal_infos[i-1]['event'] == '卖出信号' and diff_price >= 0:
                    t['event'] = '平仓亏损'
                    t['index'] = -1
                    t['price'] = '-'
                    t['gain'] = diff_price * (-1)
                    t['info'] = '亏损, 在 %.2f 点进行平仓' % now_p
                    info.append(t)
                elif signal_infos[i-1]['event'] == '卖出信号' and diff_price <= 0:
                    t['event'] = '平仓盈利'
                    t['index'] = -1
                    t['price'] = '-'
                    t['gain'] = diff_price * (-1)
                    t['info'] = '盈利, 在 %.2f 点进行平仓' % now_p
                    info.append(t)
            if i == len(signal_infos) - 1:
                info.append(signal_infos[i])
        return info

if __name__ == '__main__':
    from simplejson import loads
    import pandas as pd
    the_file = '/root/ema_backtest_data/2015-11-24_if1512_480_1200'
    df_list = loads(open(the_file).read())
    ema_df = pd.DataFrame(df_list, columns=['time_index', 'price', 'volume', 'fitting_price', 'ema_short', 'ema_long'])
    rs = SellSignal.compare_ema(ema_df)
    print len(rs)
    print SellSignal.profit_infos(rs)
