# -*- coding: utf8 -*-

from consts import EMA_LONG


class EMASignal(object):

    def __init__(self, price_list, ema_short, ema_long):
        self.price_list = price_list
        self.ema_short = ema_short
        self.ema_long = ema_long
        self.N = len(self.price_list)


    def out_put(self):
        infos = self.compare_ema()
        for i in range(len(infos)):
            infos[i]['series'] = i+1
        return infos


    def out_flags(self):
        infos = self.compare_ema()
        flags = []
        for info in infos:
            if info['index'] != -1:
                if '卖' in info['event']:
                    flags.append([info['index'], '卖', info['price']])
                elif '买' in info['event']:
                    flags.append([info['index'], '买', info['price']])
        return flags


    def compare_ema(self):
        signal_res = []
        diff_list = [(self.ema_short[i] - self.ema_long[i]) for i in range(self.N)]
        for i in range(self.N):
            if i >= EMA_LONG:
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
                    t['index'] = index2mtime(i)
                    t['price'] = self.price_list[i]
                    t['gain'] = '-' #盈利
                    t['info'] = ''
                    signal_res.append(t)

            if i == 269:
                t = {}
                t['event'] = '收盘平仓'
                t['index'] = index2mtime(i)
                t['price'] = self.price_list[i]
                t['gain'] = '-'
                t['info'] = '收盘前平仓'
                signal_res.append(t)


        info = []
        for i in range(len(signal_res)):
            diff_price = 0
            if i > 0 and i < len(signal_res):
                now_p = signal_res[i]['price']
                befo_p = signal_res[i-1]['price']
                diff_price = (now_p - befo_p) * 300
                info.append(signal_res[i-1])
                t = {}
                if signal_res[i-1]['event'] == '买入信号' and diff_price >= 0:
                    t['event'] = '平仓盈利'
                    t['index'] = -1
                    t['price'] = '-'
                    t['gain'] = diff_price
                    t['info'] = '盈利, 在 %.2f 点进行平仓' % now_p
                    info.append(t)
                elif signal_res[i-1]['event'] == '买入信号' and diff_price <= 0:
                    t['event'] = '平仓亏损'
                    t['index'] = -1
                    t['price'] = '-'
                    t['gain'] = diff_price
                    t['info'] = '亏损, 在 %.2f 点进行平仓' % now_p
                    info.append(t)
                elif signal_res[i-1]['event'] == '卖出信号' and diff_price >= 0:
                    t['event'] = '平仓亏损'
                    t['index'] = -1
                    t['price'] = '-'
                    t['gain'] = diff_price * (-1)
                    t['info'] = '亏损, 在 %.2f 点进行平仓' % now_p
                    info.append(t)
                elif signal_res[i-1]['event'] == '卖出信号' and diff_price <= 0:
                    t['event'] = '平仓盈利'
                    t['index'] = -1
                    t['price'] = '-'
                    t['gain'] = diff_price * (-1)
                    t['info'] = '盈利, 在 %.2f 点进行平仓' % now_p
                    info.append(t)
            if i == len(signal_res) - 1:
                info.append(signal_res[i])

        return info

