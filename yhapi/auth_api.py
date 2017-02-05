# -*- coding: utf8 -*-

import requests
import traceback
from ast import literal_eval
from urllib import quote_plus


from conf import (AUTH_HEADER, AUTH_DATA, AUTH_DATA_2, \
        CONN_SESS_DATA, CONN_SESS_DATA_2, \
        TRANS_URL, TRANS_HOST, \
        TRANS_AUTH_DATA_SP1, \
        TRANS_AUTH_DATA_SP2, TRANS_AUTH_DATA_ALL)
from utils import _time, _time_trans
from const import *

from api_logger import yh_api_logger


def get_auth_url():
    # ----- get ip port
    try:
        url_ip_port = 'http://wxhq.yhqh.com.cn'
        res_ip_port = requests.get(url=url_ip_port)
        cont_ip_port = res_ip_port.text
        if 'AuthAddress' in cont_ip_port:
            idx = cont_ip_port.find('AuthAddress')
            _cont = cont_ip_port[idx: idx+100]
            tmpip, tmpport = _cont.split('\r\n')[:2]
            tmpip = tmpip.split(',')[0].split(':')[1].strip()[1:-1]
            tmpport = int(tmpport.split(',')[0].split(':')[1].strip())

            auth_url = 'http://%s:%s' % (tmpip, tmpport)
    except BaseException, e:
        yh_api_logger.error(traceback.format_exc())
        auth_url = ''
    yh_api_logger.info('auth url : %s' % str(auth_url))
    return auth_url


def api_authentication(auth_url):
    try:
        # ----- auth step 1
        _header = AUTH_HEADER
        _header['Host'] = auth_url[7:]
        _timestr = _time()
        _url = auth_url + '/?%s' % _timestr
        r = requests.post(_url, data=AUTH_DATA, headers=_header)

        tmp_data = r.text.split('\r\n\r\n')
        yh_api_logger.debug(tmp_data[0])
        yh_api_logger.debug(tmp_data[1])

        # ----- auth step 2
        _header2 = AUTH_HEADER
        _header2['Host'] = auth_step_2_host_post
        _url2 = 'http://' + auth_step_2_host_post + '/?%s' % _timestr
        r2 = requests.post(_url2, data=AUTH_DATA_2, headers=_header2)

        tmp_data2 = r2.text.split('\r\n\r\n')
        yh_api_logger.debug(tmp_data2[0])
        yh_api_logger.debug(tmp_data2[1])

        tmp_dict = literal_eval(tmp_data2[1])
        connection_session = int(tmp_dict['ConnectionSession'])

        yh_api_logger.info('the ConnectionSession code is : %s' %connection_session)
    except BaseException, e:
        yh_api_logger.error(traceback.format_exc())
        connection_session = ''
    return connection_session


def api_auth_connection_session(connection_session):
    try:
        # ----- connection_session step 1
        _timestr = _time()

        _header = AUTH_HEADER
        _header['Host'] = auth_step_2_host_post
        _url = 'http://' + auth_step_2_host_post + '/?%s' % _timestr
        r = requests.post(_url, data=CONN_SESS_DATA % connection_session, headers=_header)

        tmp_data = r.text.split('\r\n\r\n')
        yh_api_logger.debug(tmp_data[0])
        yh_api_logger.debug(tmp_data[1])

        # ------ connection_session step 2
        r2 = requests.post(_url, data=CONN_SESS_DATA_2 % connection_session, headers=_header)

        tmp_data2 = r2.text.split('\r\n\r\n')
        yh_api_logger.debug(tmp_data2[0])
        yh_api_logger.debug(tmp_data2[1])

        tmp_dict = literal_eval(tmp_data2[1])
    except BaseException, e:
        yh_api_logger.error(traceback.format_exc())


def _yh_auth():
    auth_url = get_auth_url()
    if auth_url:
        connection_session = api_authentication(auth_url)
        if connection_session:
            api_auth_connection_session(connection_session)
        return connection_session
    return None

yinhe_auth = _yh_auth


def api_trans_auth_session():
    try:
        # ----- auth step 1
        _header = AUTH_HEADER
        _header['Host'] = TRANS_HOST
        _timestr = _time()
        _time_trans_str = _time_trans()
        _url = TRANS_URL % _timestr
        _d = quote_plus(TRANS_AUTH_DATA_SP1)
        trans_data = TRANS_AUTH_DATA_ALL % (_d, _time_trans_str)
        r = requests.post(_url, data=trans_data, headers=_header)

        tmp_data = literal_eval(r.text)
        print tmp_data
        trans_session = int(tmp_data['Session'])
        yh_api_logger.debug(tmp_data)
    except BaseException, e:
        yh_api_logger.error(traceback.format_exc())
        trans_session = None
    return trans_session


def api_trans_auth_check(trans_session):
    try:
        # ----- auth step 2
        check_res = False
        _header = AUTH_HEADER
        _header['Host'] = TRANS_HOST
        _timestr = _time()
        _time_trans_str = _time_trans()
        _url = TRANS_URL % _timestr
        _d2 = quote_plus(TRANS_AUTH_DATA_SP2 % trans_session)
        trans_data = TRANS_AUTH_DATA_ALL % (_d2, _time_trans_str)
        r = requests.post(_url, data=trans_data, headers=_header)

        tmp_data2 = r.text
        print tmp_data2
        if 'error_no' not in tmp_data2:
            check_res = True
        yh_api_logger.debug(tmp_data2)
    except BaseException, e:
        yh_api_logger.error(traceback.format_exc())
    return check_res

yinhe_trans = api_trans_auth_session
yinhe_trans_check = api_trans_auth_check

# test
def main():
    '''
    auth_url = get_auth_url()
    connection_session = api_authentication(auth_url)
    api_auth_connection_session(connection_session)
    '''
    api_trans_auth_session()


if __name__ == '__main__':
    main()
