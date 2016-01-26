#_*_coding:utf-8_*_
import json,time
import sconf
import rediswrap
import gzip
import utils
from mysqlwrap import dbclass
from functools import wraps
"""
错误码
510 数据配置错误
511 数据库连接错误
512 
"""
class err_handle:
    loss_arg = [-6,'缺失参数']
    gkey_not_set = [-1,'未检测到参数gkey.']
    items_not_set = [-2,'未检测到参数items']
    db_err = [-100,'数据库操作错误']
    action_not_found = [-101,'action not found']
    gkey_not_found = [-3,'gkey未注册']
    data_not_found = [-4,'未检测到参数data']
    item_exis = [-5,'item已存在']
    sphinx_param_not_set = [-10,"没有设置参数组param"]
    sphinx_index_not_found = [-11,'索引不存在']
    #-----rest状态码----#
    
    db_conf_err     =   510 #数据库配置未找到
    db_connect_err  =   511 #连接数据库失败
    
class RestStatus:
    #-----rest状态码----#
    access          =   200
    db_conf_err     =   510 #数据库配置未找到
    db_connect_err  =   511 #连接数据库失败
	
#-------参数配置文件-----#                
def get_cnf_val(k,dist):
    """递归取出joson配置信息值
    """
    if '.' not in k :
        return dist[k] if k in dist else None
    kesy = k.split('.')     
    if kesy[0] in dist:
        kk = k[k.index('.')+1:]
        tmp = dist[kesy[0]]
        return get_cnf_val(kk,tmp)
    else:
        return None
def get_host_by_data(k):
    """取出数据服务器信息
    """
    host_key = get_cnf_val(k,sconf.DATA_SOURC)
    if host_key:
        return  get_cnf_val(host_key['info'],sconf.HOST)
    return None             

def get_data_info(k):
    """取出数据库配置信息
    """
    return get_cnf_val(k,sconf.DATA_SOURC)
     
#---redis缓存---# 
def cache_get(key):
    rdb = rediswrap.get_redis('cache')
    return gzip.decompress(rdb.get(key)).decode()
def cache_set(key,val,ttl=0):
    rdb = rediswrap.get_redis('cache')
    val = gzip.compress(val.encode())
    rdb.setex(key,val,ttl)
#---mysql查询---#
def mysql(biznum):
 
    dbinfo = get_host_by_data(biznum)
 
    def on_sql_error(serr):
        status = -100
        err = str(err)
        return status,err
    def decorator(fn):
        @wraps(fn)
        def wrapper(kwargs):
            if not dbinfo:
                return err_handle.db_conf_err,
            dbinfo['dbname']=biznum.split('.')[-1]
            db = dbclass(dbinfo)
            res,desc = db.connect()
    
            if res == -1:
                return on_sql_error(desc)
            result = fn(db, **kwargs)
            if result[0] == -1:
                result = on_sql_error(result[1])
            db.close()
            return result
        return wrapper
 
    return decorator
    
def  get_table_name(id,tableprefix):
        tid = int((id+1)/5000000)+1
        return "%s_%s" %(tableprefix,tid)   
def get_table_id(table,db=None):
    desc = db.query("select max(id) as mid from %s" % table)
    maxid       = desc[0]['mid'] + 1
    return maxid
    
def mysqlrest(info): 
    dbinfo              = info['dbinfo']
    dbinfo['dbname']    = info['dbname']
    shard_table         = info['shard_table']
    def on_sql_error(serr):
        status = 512
        err = str(err)
        return status,err
    def decorator(fn):
        @wraps(fn)
        def wrapper(kwargs):
            db = dbclass(dbinfo)
            res,desc = db.connect()
            if res == -1:
                return on_sql_error(desc)
            if kwargs['table'] in shard_table:
                if "id" not in kwargs:
                    id = get_table_id(kwargs['table'],db)
                else:
                    id = kwargs['id']
                kwargs['table'] = get_table_name(id,kwargs['table'])
                    
            result = fn(db, **kwargs)
            if result[0] == -1:
                result = on_sql_error(result[1])
            db.close()
            return result
        return wrapper
 
    return decorator    
#------------注册回调函数---
def callback(myapp):
    def decorator(fn):
        name = fn.__name__
        myapp[name] = fn
        @wraps(fn)
        def wrapper(kwargs):
            return fn
        return wrapper
 
    return decorator
if __name__=="__main__":
    pass
        