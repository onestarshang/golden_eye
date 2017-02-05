#coding:utf-8

import sys
import traceback
import MySQLdb as mdb

from api_logger import yh_api_logger


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


def disconnectdb(_curs, _conn):
    try :
        _curs.close()
    except BaseException, e:
        yh_api_logger.error(traceback.format_exc())

    try :
        _conn.close()
    except BaseException, e:
        yh_api_logger.error(traceback.format_exc())


def rundb(sql, vals=[], db_conf={}, result=True):
    try :
        curs, conn = connectdb()
        curs.execute(sql , vals)
        conn.commit()
        r = None
        if result:
            r = curs.fetchall()
        return r
    except BaseException, e:
        yh_api_logger.error(traceback.format_exc())
        yh_api_logger.error(sql)
        r = None
    finally:
        disconnectdb(curs, conn)
        return r


if __name__ == '__main__':
    tt = "select * from test;"
    res = rundb(tt)
    print res
