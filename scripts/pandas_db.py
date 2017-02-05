#coding:utf-8

import sys
import traceback
import MySQLdb as mdb


DB = 'yh_data'
HOST = '127.0.0.1'
UID = 'root'
PWD = 'onestar'
PORT_NUM = 3306
CHARCODE = 'utf8'

#test_db
#--------------------------------------------------------------
def connectdb():
    _db = DB
    _host = HOST
    _port = PORT_NUM
    _uid = UID
    _pwd = PWD
    _charcode = CHARCODE
    #连接mysql的方法：connect('ip','user','password','dbname')
    conn =  mdb.connect(_host, _uid, _pwd, _db, charset=_charcode)
    curs = conn.cursor()
    return curs, conn

yhdb = connectdb()[1]
