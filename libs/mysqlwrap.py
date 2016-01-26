#_*_coding:utf-8_*_

# Copyright (c) 2008 crunch <hymm91@gmail.com>
# All rights reserved

#$Id: dbclass.py 649 2009-11-19 09:31:37Z robble $#
__author__ = 'crunch <hymm91@gmail.com>'
__version__ = '$Revision: 0.1 $'

try:
    import MySQLdb
except ImportError:
    import pymysql as MySQLdb

import sys
import os,time
import pdb
from threading import Thread
import traceback
import random
DEFAULT_ENCODING = 'utf8' # sys.getdefaultencoding()
#--- System mysqldb ----------------------------------------------
DBPOOL = {
    'default': None
}

def pool_monitor():
    """启动连接池守护进程
    """
    global DBPOOL
    for k in DBPOOL.keys():
        if hasattr(DBPOOL[k],'_conn'):
            res ,desc = DBPOOL[k].connect()
            if res == -1:
                print(DBPOOL[k]._dbinfo)
                raise Exception(desc)
    pd = P_monitor()
    pd.setDaemon(True)
    pd.start()
    return pd

def setup_db(name,kw):
    """
    注册数据库连接
    """
    db = dbclass(kw)
    res ,desc = db.connect()
    if res ==0:
        DBPOOL[name]=db
    return res,desc
def get_db(name='default'):
    """获取数据库接
    """
    return DBPOOL.get(name,None)

def random_db():
    """随机取一个连接
    """
    return random.sample(DBPOOL,1)
    
def escape_string(val):
    return MySQLdb.escape_string(val)

def structure_sql(item):
    """将查询语句的字典结构转换为sql
    """
    #assert(item,(tuple,list))
    if 'fields' in item and item['fields']:
    	pass
    else:
        item['fields'] = '*'    
    sql = "select %s from %s" %(item['fields'] ,item['table'])
    if 'where' in item and item['where']:
        sql = "%s where %s" % (sql,item['where'])
    if 'group' in item and item['group']:
        sql = "%s group by %s" % (sql,item['group'])
    if 'order' in item and item['order']:
        sql = "%s order by %s" % (sql,item['order'])
    if 'limit' in item and item['limit']:
        sql = "%s limit %s" % (sql,item['limit'])
    return sql


class P_monitor(Thread):
    """连接池守护进程
    """
    def __init__(self):
        super(P_monitor, self).__init__()
        
    def run(self):
        while 1:
            try:
                for k in DBPOOL.keys():
                    if hasattr(DBPOOL[k],'_conn') and DBPOOL[k]._conn:
                        try:
                            #DBPOOL[k]._conn.ping(reconnect=False)
                            DBPOOL[k]._conn.ping()
                        except:
                            traceback.print_exc()
                            DBPOOL[k].connect()
                    elif hasattr(DBPOOL[k],'_conn'):
                        res, desc =DBPOOL[k].connect()
                        if res == -1:
                            print(desc)
            except Exception as e:
                traceback.print_exc()
            time.sleep(5)
        
class dbclass:
    ''' @dbinfo {'host':'192.168.0.1','port':3360,'dbname':'test',
                    'user':'root','passwd':'123','charset':'utf8'}
    '''
    def __init__(self, db_info):
        self._conn = None
        self._cursor = None
        self._dbinfo =  db_info
        self._sleeptime = int(time.time())
        
    def connect(self,db_info={}):
        assert(type(db_info) == dict)
        db_info = db_info or self._dbinfo
        charset = db_info.get('charset',DEFAULT_ENCODING)
        dbname = db_info.get('dbname','')

        try:
            #XXX 端口号没写？
            self._conn =MySQLdb.connect(db_info['host'],db_info['user'],db_info['passwd'],dbname,int(db_info['port']))
            self._conn.set_charset(charset)
            self._conn.autocommit(1) #自动提交
            self._cursor = self._conn.cursor(MySQLdb.cursors.DictCursor)
            self._cursor.execute("set names '%s';" % charset)
        except MySQLdb.Error as e:
            return (-1, e)
            
        return (0, None)

    def escape_string(self, val):
        return MySQLdb.escape_string(val)

    def select_db(self,dbname):
        self._conn.select_db(dbname)
    def query(self, sql,mod=0, param=None):
        #pdb.set_trace()
        t = time.time()
        if t - self._sleeptime > 10:
            self._conn.ping()
        self._sleeptime = t
        if type(sql) == dict:
            sql = structure_sql(sql)
        try:
            if not param:
                rs=self._cursor.execute(sql)
            else:
                rs=self._cursor.execute(sql, param)
            if mod==1:
                self._conn.commit()
                return (0,rs)
            infos = self._cursor.fetchall()
        
        except MySQLdb.err.OperationalError as e:
            if e.args[0] == 2013:    
                self.connect()
            return (-1, list(e))
        except UnicodeDecodeError as e:
            return (-1, e)
        except UnicodeEncodeError as e:
            return (-1, e)
        except Exception as e:
            #traceback.print_exc()
            return (-1, e.args)
        return (0, infos)


    def insert(self,tbname,data,mod=0):
        assert (isinstance(data, dict))
        fields = []
        values = []
        for k,v in data.items():
            fields.append(k)
            values.append("'%s'" % v)
        sql = "insert into %s(%s)values(%s)" % (tbname,','.join(fields),','.join(values))
        res,desc = self.query(sql,mod)
        if res == 0:
            return [0,int(self._cursor.lastrowid)]
        return res,desc
    def update(self,tbname,setdata,where='',mod=0):
        if not where:
            id = setdata.pop('id')
            where = "id=%s"% id
        set_str = ",".join(["%s='%s'"%(k,v) for k,v in setdata.items()])
        sql = "update %s set %s where %s" %(tbname,set_str,where)
        res,desc = self.query(sql,mod)
        if res ==0:
            return [0,self._cursor.rowcount]
        return res,desc    
    def delete(self,tbname,where='',mod=0):
        if not where:
            id = setdata.pop('id')
            where = "id=%s"% id
        sql = "delete from %s where %s" %(tbname,where)
        res,desc = self.query(sql,mod)
        if res ==0:
            return [0,self._cursor.rowcount]
        return res,desc      
    def close(self):
        try:
            if self._conn:
                self._conn.close()
                self._conn = None
            if self._cursor:
                self._cursor.close()
                self._cursor = None
        except:
            pass

def addslashes(s):
    """特殊字符转义
    """
    #t1 = time.time()
    l = ["\\", '"', "'", "\0", ]
    for i in l:
        if i in s:
            s = s.replace(i, '\\'+i)
    #print time.time() - t1
    return s
        
if __name__ == '__main__':
    #数据库连接信息
    dbinfo ={'host':'192.168.10.126','port':3306,'dbname':'statsys',
            'user':'wbsp','passwd':'wbsp','charset':'utf8'}
    #注册入连接池
    setup_db('default',dbinfo)
    #启动连接池守护进程
    pool_monitor()
    #获取一个数据连接
    db = get_db('default')
    while 1:
        print(get_db().query('show tables'))
        time.sleep(60)
    """
    #print(info.query("show databases"))
    v = {'name':'李四','job':'设计师','ag':35}
    import json
    d = json.dumps(v)
    sql = "insert into t(name)values('%s')" % addslashes(d)
    sql = "select name from t"
    res,desc=info.query(sql)
    for row in desc:
        print(row)
        print(json.loads(row['name']))
    """


    
