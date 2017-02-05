# -*- coding: utf8 -*-

# authentication step 1
'''
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded; charset=UTF-8;
Referer: http://wxhq.yhqh.com.cn/
Content-Length: 266
Origin: http://wxhq.yhqh.com.cn
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache
'''

AUTH_HEADER = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8;',
        'Referer': 'http://wxhq.yhqh.com.cn/',
        'Origin': 'http://wxhq.yhqh.com.cn',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
        }

AUTH_DATA = '''3,226,0,1,1,0,0,0,0\r\n\r\n<?xml version="1.0" encoding="utf-8" standalone="yes" ?><XMLDATA version="1.0" data="UserAuth"><Auth Na='V211' Pa='123' Pr='H5' CarType='1' CR='1' SR='1' BM='1' UR='13' UD='1,2'  OD='1001,1002' SER='TD,NS,QT'></Auth></XMLDATA>'''
AUTH_DATA_2 = '''3,239,0,2,1,0,0,0,0,0,0\r\n\r\n{"User":"V211","Pass":"123","AuthSerID":13,"UserID":388630,"Session":8980079,"Product":1,"SubProduct":109,"Block":[],"Market":[3000,3001,3002,3003,4000,16000,16001,16002,9000,9001,10000,10001,11000,13000,13001,12000,7000,8000,0,1000,3009]}'''

# AUTH CONNECTION SESSION
CONN_SESS_DATA = '''3,19,0,56,2,0,0,0,0,%s,0\r\n\r\n{"Req":"SubMarket"}'''
CONN_SESS_DATA_2 = '''3,19,0,59,3,0,0,0,0,%s,0\r\n\r\n[{"TradeTimeID":0}]'''


#*****************************************************************************
#PRICE DATA
TRANS_DATA = '''3,78,0,52,384,0,0,0,0,%s,0\r\n\r\n{"MarketID":3003,"IDType":1,"BeginPos":%s,"Count":%s,"GetQuote":1,"PushFlag":0}'''
PRICE_DATA = '''3,638,0,153,15,0,0,0,0,%s,0\r\n\r\n{"PushFlag":0,"GetSymInfo":1,"Symbol":[{"Market":3003,"Code":"040120","Net":"DZNET"},{"Market":3003,"Code":"040121","Net":"DZNET"},{"Market":3003,"Code":"040122","Net":"DZNET"},{"Market":3003,"Code":"040123","Net":"DZNET"},{"Market":3003,"Code":"040188","Net":"DZNET"},{"Market":3003,"Code":"040190","Net":"DZNET"},{"Market":3003,"Code":"040101","Net":"DZNET"},{"Market":3003,"Code":"040102","Net":"DZNET"},{"Market":3003,"Code":"040103","Net":"DZNET"},{"Market":3003,"Code":"040104","Net":"DZNET"},{"Market":3003,"Code":"040105","Net":"DZNET"},{"Market":3003,"Code":"040106","Net":"DZNET"},{"Market":3003,"Code":"040107","Net":"DZNET"}]}'''

PRICE_HISTORY_DATA = '''3,113,0,152,557,0,0,0,0,%s,0\r\n\r\n{"Market":3003,"Code":"040120","PushFlag":0,"TimeType":0,"TimeValue0":75,"TimeValue1":435,"Day":"2015-8-7 0:0:0"}'''

PRICE_SECOND_DATA = '''3,86,0,153,560,0,0,0,0,%s,0\r\n\r\n{"PushFlag":0,"GetSymInfo":1,"Symbol":[{"Market":3003,"Code":"%s","Net":"DZNET"}]}'''



#*****************************************************************************
#交易验证

TRANS_URL = 'http://27.115.78.45/HTTP/Service.aspx?%s'
TRANS_HOST = '27.115.78.45'
#test
TRANS_AUTH_DATA_ALL = '''Data=%s&TradeAddress=114.255.82.175&TradePort=40135&ran=%s'''
TRANS_AUTH_DATA_SP1 = '''{"Function":200,"Session":0,"ColumnNames":"account,password","RowValues":["userid,password"]}'''

TRANS_AUTH_DATA_SP2 = '''{"Function":200,"Session":%s,"ColumnNames":"account,password","RowValues":["userid,password"]}'''


# 交易

LONG_SHORT_DATA = '''{"Function":301,"Session":"%s","ColumnNames":"exchange_type,stock_code,entrust_price,entrust_amount,entrust_bs,eo_flag,sh_flag,stock_account,fund_account,password","RowValues":["F4,%s,%s,%s,%s,%s,0,userid,userid,password"]}'''
