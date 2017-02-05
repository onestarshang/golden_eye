#-*- coding: utf8 -*-

import sys, os
from os.path import dirname
sys.path.insert(0, dirname(dirname(os.path.abspath(__file__))))

import time
import traceback
from datetime import datetime, timedelta, date
import pandas as pd
import simplejson

from yhapi.utils import UTC_time, ifcode_map
from yhapi.mongodb_mod import yh_mongodb
from yhapi.api_logger import yh_api_logger
from yhapi.transaction_api import (yinhe_trans, trans_short_start,
                                   trans_long_close, trans_long_start,
                                   trans_short_close)
from sell_signals.push_signal import PushSellSignal
from indicator import Indicator
from consts import old_infos_dir
from libs.utils import str2day

from push_it import push_sig


column_key = ['InsertTime', 'Time', 'Now', 'Open',\
              'High', 'Low', 'CurHold', 'Hold',\
              'Volume', 'BuyVolume', 'SellVolume', 'VolumeRate']


def is_push(new_infos, ifcode, today):
    _file = '%s/%s_%s' % (old_infos_dir, ifcode, today)
    old_infos = []
    if not os.path.isfile(_file): # init
        f = open(_file, 'w')
        try:
            f.write(simplejson.dumps(new_infos))
            f.close()
        except BaseException, e:
            tip = '写信号文件失败'
            push_sig(tip)
            f.close()
            return False
        return True
    else:
        f = open(_file)
        try:
            old_infos = simplejson.loads(f.read())
            f.close()
        except BaseException, e:
            tip = '读信号文件失败'
            push_sig(tip)
            f.close()
            return False
        if len(new_infos) != len(old_infos):
            f = open(_file, 'w')
            try:
                f.write(simplejson.dumps(new_infos))
                f.close()
            except BaseException, e:
                tip = '写信号文件失败'
                push_sig(tip)
                f.close()
                return False
            return True
    return False


def realtime_data(ifcode, code, today, coll):
    year, month, day = today.year, today.month, today.day
    datetime_s1 = datetime(year, month, day, 9, 15, 00)
    datetime_e1 = datetime(year, month, day, 11, 30, 00)
    datetime_s2 = datetime(year, month, day, 13, 00, 00)
    datetime_e2 = datetime(year, month, day, 15, 15, 00)
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
            _t = [tmp[1], tmp[2], tmp[8]]
            rs.append(_t)
    return rs


def push_signal(df_list, code, ifcode, today, period_short, period_long):
    df = pd.DataFrame(df_list, columns=['time_index', 'price', 'volume'])
    price = list(df['price'])
    df['ema_short'] = Indicator.ema_metric(period_short, price)
    df['ema_long'] = Indicator.ema_metric(period_long, price)
    sig_infos = PushSellSignal.compare_ema(df)
    profit_infos = PushSellSignal.profit_infos(sig_infos)
    if is_push(profit_infos, ifcode, today):
        if len(profit_infos) == 1:
            print '*'*20
            print 'init message~!'
            time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            info_dict = profit_infos[0]
            theevent = info_dict.get('event', '')
            is_success = 'failed'
            #添加交易接口
            if theevent == '卖出信号':
                trans_session = yinhe_trans()
                r = trans_short_start(trans_session, code, ifcode)
                if 'error_info' not in r:
                    is_success = '交易成功'
            elif theevent == '买入信号':
                trans_session = yinhe_trans()
                r = trans_long_start(trans_session, code, ifcode)
                if 'error_info' not in r:
                    is_success = '交易成功'
            tip = 'ema 策略: \n%s, 交易价格: %s; 时间: %s; %s' % (theevent,
                                                  info_dict.get('price', 0),
                                                  time_str, is_success)
            push_sig(tip)
        elif len(profit_infos) >= 2:
            print '*'*20
            print 'push message~!'
            time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            info_dict_1 = profit_infos[-2]
            info_dict_2 = profit_infos[-1]
            _p = info_dict_2.get('price', 0)
            trading_fee = cal_fee(_p)
            _g = info_dict_1.get('gain', 0)
            gain = _g - trading_fee

            theevent = info_dict_2.get('event', '')
            is_success = 'failed'
            #添加交易接口
            if theevent == '卖出信号':
                trans_session = yinhe_trans()
                r1 = trans_short_close(trans_session, code, ifcode)
                r2 = trans_short_start(trans_session, code, ifcode)
                if 'error_info' not in r1 and 'error_info' not in r2:
                    is_success = '交易成功'
            elif theevent == '买入信号':
                trans_session = yinhe_trans()
                r1 = trans_long_close(trans_session, code, ifcode)
                r2 = trans_long_start(trans_session, code, ifcode)
                if 'error_info' not in r1 and 'error_info' not in r2:
                    is_success = '交易成功'
            tip = 'ema 策略: \n%s, 盈利: %s, 实际盈利: %s, 交易费用: %s; \n%s, 交易价格: %s; 时间: %s; %s' % (info_dict_1.get('event', ''),
                                                  _g,
                                                  gain,
                                                  trading_fee,
                                                  info_dict_2.get('event', ''),
                                                  _p,
                                                  time_str,
                                                  is_success)
            push_sig(tip)


def cal_fee(price):
    return price*1.0*300/10000*23


def main(ifcode, code, period_short, period_long):
    today = date.today()
    year, month, day = today.year, today.month, today.day
    datetime_start = datetime(year, month, day, 9, 00, 00)
    datetime_end = datetime(year, month, day, 15, 00, 00)
    datetime_now = datetime.now()

    coll_name = '%s_data_second' % ifcode.lower()
    coll = yh_mongodb[coll_name]

    #df_list = realtime_data(ifcode, code, today)
    #push_signal(df_list, ifcode, today, period_short, period_long)

    while True:
        try:
            if datetime_now > datetime_start and datetime_now <= datetime_end:
                df_list = realtime_data(ifcode, code, today, coll)
                #print '*'*20
                #print len(df_list)
                try:
                    push_signal(df_list, code, ifcode, today, period_short, period_long)
                except BaseException, e:
                    print traceback.format_exc()
            else:
                break
        except BaseException, e:
            yh_api_logger.error(traceback.format_exc())
        datetime_now = datetime.now()
        time.sleep(3)


if __name__ == '__main__':
    arg = sys.argv
    ifcode, code, period_short, period_long = arg[1:]
    #ifcode, code = 'IF1509', '040109'
    main(ifcode, code, int(period_short), int(period_long))
