# -*- coding: utf8 -*-


class TradingSignal(object):

    @classmethod
    def trading_sig(cls, df, is_backtest, offset_long, limit_period=1000):
        time_index = list(df['time_index'])
        price = list(df['price'])
        metric_short = list(df['ema_short'])
        metric_long = list(df['ema_long'])
        return self._signals(time_index, price, metric_short,
                             metric_long, is_backtest, offset_long,
                             limit_period)

    def _signals(self, time_index, price, metric_short, metric_long,
                is_backtest, offset_long, limit_period):
        signal_infos = []
        price_num = len(price)
        diff_list = [(metric_short[i] - metric_long[i]) for i in range(price_num)]
        for i in range(price_num):
            if i >= offset_long:
                _s = diff_list[i-1]
                _sa = diff_list[i]
                if (_s * _sa) <= 0:
                    t = {}
                    if _s > 0 and _sa <= 0:
                        t['trading_event'] = '卖出信号'
                    elif _s < 0 and _sa >= 0:
                        t['trading_event'] = '买入信号'
                    else:
                        continue
                    t['time_index'] = time_index[i]
                    t['trading_price'] = price[i]
                    t['trading_profit'] = -1 # 默认为-1
                    signal_infos.append(t)
            if is_backtest and i > price_num - limit_period:
                t = {}
                t['trading_event'] = '收盘平仓'
                t['time_index'] = time_index[i]
                t['trading_price'] = price[i]
                t['trading_profit'] = -1
                signal_infos.append(t)
                break

        return signal_infos

    @classmethod
    def profit_infos(cls, signal_infos):
        info = []
        for i in range(len(signal_infos)):
            diff_price = 0
            if i > 0 and i < len(signal_infos):
                now_p = signal_infos[i]['trading_price']
                befo_p = signal_infos[i-1]['trading_price']
                diff_price = (now_p - befo_p) * 300
                info.append(signal_infos[i-1])

                t = {'time_index': -1, 'trading_price': '-',
                     'trading_profit': diff_price}

                if signal_infos[i-1]['trading_event'] == '买入信号' and diff_price >= 0:
                    t['trading_event'] = '平仓盈利'
                    t['trading_message'] = '盈利, 在 %.2f 点进行平仓' % now_p
                    info.append(t)
                elif signal_infos[i-1]['trading_event'] == '买入信号' and diff_price <= 0:
                    t['trading_event'] = '平仓亏损'
                    t['trading_message'] = '亏损, 在 %.2f 点进行平仓' % now_p
                    info.append(t)
                elif signal_infos[i-1]['trading_event'] == '卖出信号' and diff_price >= 0:
                    t['trading_event'] = '平仓亏损'
                    t['trading_message'] = '亏损, 在 %.2f 点进行平仓' % now_p
                    info.append(t)
                elif signal_infos[i-1]['trading_event'] == '卖出信号' and diff_price <= 0:
                    t['trading_event'] = '平仓盈利'
                    t['trading_message'] = '盈利, 在 %.2f 点进行平仓' % now_p
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
