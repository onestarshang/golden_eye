# -*- coding: utf8 -*-

ema_file_dir = '/path/to/ema_backtest_data'
old_infos_dir = '/path/to/ema_infos'
validate_df_dir = '/path/to/df_data'
old_infos_dir_macd = '/path/to/macd_infos'
macd_file_dir = '/path/to/macd_backtest_data'
trans_session_dir = '/path/to/trans_session'
macd_param_analysis_dir = '/path/to/macd_param_analysis'

from datetime import datetime
'''
原始交割日期
jiaoge = {'if1601' : [datetime(2015, 12, 19), datetime(2016, 1, 15)],
          'if1602' : [datetime(2016, 1, 16), datetime(2016, 2, 19)],
          'if1603': [datetime(2016, 2, 20), datetime(2016, 3, 18)],
          'if1604': [datetime(2016, 3, 19), datetime(2016, 4, 15)],
          'if1605': [datetime(2016, 4, 16), datetime(2016, 5, 20)],
          'if1606': [datetime(2016, 5, 21), datetime(2016, 6, 17)],
          'if1607': [datetime(2016, 6, 18), datetime(2016, 7, 15)],
          'if1608': [datetime(2016, 7, 16), datetime(2016, 8, 19)],
          'if1609': [datetime(2016, 8, 20), datetime(2016, 9, 16)],
          'if1610': [datetime(2016, 9, 17), datetime(2016, 10, 21)],
          'if1611': [datetime(2016, 10, 22), datetime(2016, 11, 18)],
          'if1612': [datetime(2016, 11, 19), datetime(2017, 12, 16)]
          }
'''
jiaoge = {'if1601' : [datetime(2015, 12, 19), datetime(2016, 1, 15)],
          'if1602' : [datetime(2016, 1, 16), datetime(2016, 2, 19)],
          'if1603': [datetime(2016, 2, 20), datetime(2016, 3, 14)],
          'if1604': [datetime(2016, 3, 15), datetime(2016, 4, 15)],
          'if1605': [datetime(2016, 4, 16), datetime(2016, 5, 20)],
          'if1606': [datetime(2016, 5, 21), datetime(2016, 6, 17)],
          'if1607': [datetime(2016, 6, 18), datetime(2016, 7, 15)],
          'if1608': [datetime(2016, 7, 16), datetime(2016, 8, 19)],
          'if1609': [datetime(2016, 8, 20), datetime(2016, 9, 16)],
          'if1610': [datetime(2016, 9, 17), datetime(2016, 10, 21)],
          'if1611': [datetime(2016, 10, 22), datetime(2016, 11, 18)],
          'if1612': [datetime(2016, 11, 19), datetime(2017, 12, 16)]
          }
init_point = 8
init_time = '34'
init_offset = 14
