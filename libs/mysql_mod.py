#-*- coding:utf8 -*-


import MySQLdb as mdb
from const import DATABASE_CONF


def connectdb():
    _host, _db, _uid, _pwd, _port = DATABASE_CONF.split(':')
    conn =  mdb.connect(_host, _uid, _pwd, _db, charset='utf8')
    curs = conn.cursor()
    return curs , conn


def disconnectdb(_curs,_conn):
    try :
        _curs.close()
    except BaseException , e :
        pass

    try :
        _conn.close()
    except BaseException , e :
        pass


def rundb(sql, vals=[] , db_conf={}, result=True):
    try :
        curs , conn = connectdb()
        curs.execute(sql , vals)
        conn.commit()
        r = None
        if result :
            r = curs.fetchall()
        return r
    except BaseException , e :
        print e
        print sql
        r = None
    finally:
        disconnectdb(curs, conn)
        return r

yhdb = rundb

if __name__ == '__main__':
    #tt = "select * from tag_users where name like '%%"+name+"%%'"

    tt2 = """select * from if1511 limit 1;"""
    res = yhdb(tt2)
    print res
