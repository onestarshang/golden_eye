#-*- coding: utf8 -*-

import requests
import traceback
from ast import literal_eval
from urllib import quote_plus
import time

from auth_api import yinhe_auth, yinhe_trans, yinhe_trans_check
from conf import (AUTH_HEADER, TRANS_DATA, PRICE_DATA, \
        PRICE_HISTORY_DATA, PRICE_SECOND_DATA, \
        TRANS_URL, TRANS_HOST, TRANS_AUTH_DATA_ALL, \
        LONG_SHORT_DATA)
from const import *
from utils import _time, _time_trans

from api_logger import yh_api_logger


# 如果需要登录会返回：
# 返回值是：1,53,53,300,384,0,0,0,0,210305,2015-8-7 6:47:32\r\n\r\n{"ReqType":52,"ErrType":2,"ErrMsg":"你需要登录"}

def api_transactions(connection_session, start_index, end_index):
    try:
        _header = AUTH_HEADER
        _header['Host'] = auth_step_2_host_post
        _timestr = _time()
        _url = 'http://' + auth_step_2_host_post + '/?%s' % _timestr
        r = requests.post(_url, data=(TRANS_DATA % (connection_session, start_index, end_index)), headers=_header)

        tmp_data = r.text.split('\r\n\r\n')
        yh_api_logger.debug(tmp_data[0])
        yh_api_logger.debug(tmp_data[1])

        tmp_dict = literal_eval(tmp_data[1])
        if 'ErrMsg' in tmp_dict:
            if tmp_dict['ErrMsg'] == '你需要登录':
                yh_api_logger.error(tmp_dict)
        return tmp_dict
    except BaseException, e:
        yh_api_logger.error(traceback.format_exc())
        return None


def api_price(connection_session):
    try:
        _header = AUTH_HEADER
        _header['Host'] = auth_step_2_host_post
        _timestr = _time()
        _url = 'http://' + auth_step_2_host_post + '/?%s' % _timestr
        r = requests.post(_url, data=(PRICE_DATA % connection_session), headers=_header)

        tmp_data = r.text.split('\r\n\r\n')
        yh_api_logger.debug(tmp_data[0])
        yh_api_logger.debug(tmp_data[1])

        tmp_dict = literal_eval(tmp_data[1])
        if 'ErrMsg' in tmp_dict:
            if tmp_dict['ErrMsg'] == '你需要登录':
                yh_api_logger.error(tmp_dict)
    except BaseException, e:
        yh_api_logger.error(traceback.format_exc())


def api_price_history(connection_session):
    #没有最高最低，只有每秒的价格等
    try:
        _header = AUTH_HEADER
        _header['Host'] = auth_step_2_host_post
        _timestr = _time()
        _url = 'http://' + auth_step_2_host_post + '/?%s' % _timestr
        r = requests.post(_url, data=(PRICE_HISTORY_DATA % connection_session), headers=_header)

        tmp_data = r.text.split('\r\n\r\n')
        yh_api_logger.debug(tmp_data[0])
        yh_api_logger.debug(tmp_data[1])

        tmp_dict = literal_eval(tmp_data[1])
        if 'ErrMsg' in tmp_dict:
            if tmp_dict['ErrMsg'] == '你需要登录':
                yh_api_logger.error(tmp_dict)
        else:
            yh_api_logger.info(tmp_dict['Trend'][-1])

            return tmp_dict
    except BaseException, e:
        yh_api_logger.error(traceback.format_exc())
    return None


def api_price_second(code, connection_session):
    '''
    return :
    Market 3003：代表中金所
    code、TradeCode：合约code
    name：合约名字
    now：最新价格
    open：开盘价
    high：最高价
    low：最低价
    avg：均价
    Settle：结算价
    CurVolume：现手
    BuyPrice0:买价
    BuyVol0:买量
    SellPrice0:卖价
    SellVol0:卖量
    Hold:持仓
    '''
    try:
        _header = AUTH_HEADER
        _header['Host'] = auth_step_2_host_post
        _timestr = _time()
        _url = 'http://' + auth_step_2_host_post + '/?%s' % _timestr
        r = requests.post(_url, data=(PRICE_SECOND_DATA % (connection_session, code)), headers=_header)

        tmp_data = r.text.split('\r\n\r\n')
        yh_api_logger.debug(tmp_data[0])
        yh_api_logger.debug(tmp_data[1])

        tmp_dict = literal_eval(tmp_data[1])
        if 'ErrMsg' in tmp_dict:
            if tmp_dict['ErrMsg'] == '你需要登录':
                yh_api_logger.error('%s: %s \n 需要登录', code, tmp_data)
        elif 'Symbol' in tmp_dict:
            _d = tmp_dict['Symbol'][0]
            yh_api_logger.info(_d)
            return _d
    except BaseException, e:
        yh_api_logger.error('%s : %s', code, traceback.format_exc())
    return None


yinhe_price_history = api_price_history
yinhe_price_second = api_price_second


def price_times(code, try_num=5):
    tick = 0
    tick_time = 0.5
    res_price = None
    while tick < try_num:
        connection_session = yinhe_auth()
        res_price = yinhe_price_second(code, connection_session)
        if res_price:
            break
        tick += 1
        time.sleep(0.2 * tick)
    return res_price

#**********************************************************
#进行交易
# 开仓做空
# entrust_amount:委托数量, eo_flag=0 表示开仓
def trans_short_start(trans_session, code, ifcode, entrust_amount=1, eo_flag=0):
    try:
        _header = AUTH_HEADER
        _header['Host'] = TRANS_HOST
        _timestr = _time()
        _time_trans_str = _time_trans()
        _url = TRANS_URL % _timestr

        res_price = price_times(code)
        buy_price = res_price['BuyPrice0']

        _d = quote_plus(LONG_SHORT_DATA % (trans_session, ifcode, buy_price, entrust_amount, 'S', eo_flag))
        trans_data = TRANS_AUTH_DATA_ALL % (_d, _time_trans_str)
        r = requests.post(_url, data=trans_data, headers=_header)

        tmp_data = r.text
        yh_api_logger.debug(tmp_data)
    except BaseException, e:
        tmp_data = 'error_info: %s' % e
        yh_api_logger.error(traceback.format_exc())
    return tmp_data


# 平仓做多
# entrust_amount:委托数量, eo_flag=1 表示平仓
def trans_long_close(trans_session, code, ifcode, entrust_amount=1, eo_flag=1):
    try:
        _header = AUTH_HEADER
        _header['Host'] = TRANS_HOST
        _timestr = _time()
        _time_trans_str = _time_trans()
        _url = TRANS_URL % _timestr

        res_price = price_times(code)
        sell_price = res_price['SellPrice0']

        _d = quote_plus(LONG_SHORT_DATA % (trans_session, ifcode, sell_price, entrust_amount, 'B', eo_flag))
        trans_data = TRANS_AUTH_DATA_ALL % (_d, _time_trans_str)
        r = requests.post(_url, data=trans_data, headers=_header)

        tmp_data = r.text
        yh_api_logger.debug(tmp_data)
    except BaseException, e:
        tmp_data = 'error_info: %s' % e
        yh_api_logger.error(traceback.format_exc())
    return tmp_data


# 开仓做多
# entrust_amount:委托数量, eo_flag=0 表示开仓
def trans_long_start(trans_session, code, ifcode, entrust_amount=1, eo_flag=0):
    try:
        _header = AUTH_HEADER
        _header['Host'] = TRANS_HOST
        _timestr = _time()
        _time_trans_str = _time_trans()
        _url = TRANS_URL % _timestr

        res_price = price_times(code)
        sell_price = res_price['SellPrice0']

        _d = quote_plus(LONG_SHORT_DATA % (trans_session, ifcode, sell_price, entrust_amount, 'B', eo_flag))
        trans_data = TRANS_AUTH_DATA_ALL % (_d, _time_trans_str)
        r = requests.post(_url, data=trans_data, headers=_header)

        tmp_data = r.text
        yh_api_logger.debug(tmp_data)
    except BaseException, e:
        tmp_data = 'error_info: %s' % e
        yh_api_logger.error(traceback.format_exc())
    return tmp_data


# 平仓做空
# entrust_amount:委托数量, eo_flag=1 表示平仓
def trans_short_close(trans_session, code, ifcode, entrust_amount=1, eo_flag=1):
    try:
        _header = AUTH_HEADER
        _header['Host'] = TRANS_HOST
        _timestr = _time()
        _time_trans_str = _time_trans()
        _url = TRANS_URL % _timestr

        res_price = price_times(code)
        buy_price = res_price['BuyPrice0']

        _d = quote_plus(LONG_SHORT_DATA % (trans_session, ifcode, buy_price, entrust_amount, 'S', eo_flag))
        trans_data = TRANS_AUTH_DATA_ALL % (_d, _time_trans_str)
        r = requests.post(_url, data=trans_data, headers=_header)

        tmp_data = r.text
        yh_api_logger.debug(tmp_data)
    except BaseException, e:
        tmp_data = 'error_info: %s' % e
        yh_api_logger.error(traceback.format_exc())
    return tmp_data


def main():
    connection_session = yinhe_auth()
    api_transactions(connection_session)
    api_price(connection_session)
    api_price_history(connection_session)
    res_price = api_price_second(connection_session)
    import pprint
    pprint.pprint(res_price)


def test_trans():
    import time
    trans_session = yinhe_trans()
    if yinhe_trans_check(trans_session):
        print trans_session
    #r = trans_short_start(trans_session, '040102', 'IF1602')
    r = trans_long_close(trans_session, '040102', 'IF1602')
    #trans_long_start(trans_session, '040102', 'IF1602')
    #r = trans_short_close(trans_session, '040102', 'IF1602')
    print r


if __name__ == '__main__':
    #main()
    test_trans()
