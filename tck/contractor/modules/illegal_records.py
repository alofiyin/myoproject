#_*_coding:utf-8_*_
# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#过滤非法关键词 
#$Id: worker.py 649 2015-06-18 fiyin $#
from  mysqlwrap import *
from rediswrap import *
from commands_ import *
import time, os
from datamodel import *

def run(*ag , **kw):
    dbsource  = get_conn_hash()
    _input    = kw.get('input')
    sql_item  = _input.get('data')
    if 'weight' not in sql_item:
         return json_dumps({"status":1,"info":"未设置input的weight字段!"})
    if 'where' not in sql_item:
        sql_item['where']=''
    job      = 'words_for_db' 
    _output  = kw.get('output')
    #测试模式,复制一个临时表
    istest = _output.pop('istest',False)
    if istest:
        tb = _output['table']+'_copy'
        #kw['output']['table']=kw['output']['table']+'_copy'
        dbinfo = dbsource.get(_output['dbserver'])['info']
        dbinfo['dbname'] = _output['dbname']
        setup_db('output',dbinfo)
        db       = get_db('output')
        db.connect()
        res,desc = db.query("show tables like '%s'" % tb )
        
        if res==0 and not desc:
            res,desc = db.query("show create table %s" % _output['table'])
            create_sql = desc[0]['Create Table'].replace('`%s`'% _output['table'] ,'`%s`' % tb).replace('\n','')
            res,desc = db.query(create_sql)
        else:
            db.query('TRUNCATE TABLE %s' % tb)
        kw['output']['table']=tb

        #truncate
    #确定数据范围
    try:
        minid, maxid = sql_item['range']
        if not minid and not maxid:
            raise Exception("no data")
    except:
        setup_db('input',dbsource.get(_input['dbserver'])['info'])
        db.connect()
        sql = "select min(id) as min,max(id) as max from %s " % (sql_item['table'])
        res, desc = get_db('input').qurey(sql)
        if res ==-1 :
            raise desc
        minid, maxid = (desc[0]['min'], desc[0]['max'])
    
    #取得符合条件的worker
    workers = get_task_workers(job=job)
    if not workers:
        #raise Exception("no worker Standby!")
        return json_dumps({"status":-1,"info":"no worker Standby!"})
    #分配任务
    split_type = sql_item.get('split_type',2)
    totle = maxid - minid +1
    step = totle/len(workers)
    #发布任务，（是否要根据workers的cup数来分配工作？）
    i = 1
    sub_taskids=[]

    sid = minid
    sql_where = sql_item['where']
    _kw = kw
    for w in workers:
        _kw['func'] = job
        _kw['input'] = _input
        if split_type == 2 and len(workers)>1:
            sid = minid
            mxid  = maxid
            if sql_where:
                _kw['input']['data']['where']="%s and mod(id,%s)=0" % (sql_where,i)
            else:
                _kw['input']['data']['where'] = " mod(id,%s)=0 " % i
        else:
            mxid = sid+step
            if w == workers[-1]:
                mxid = maxid
                
        _kw['input']['data']['range'] = (sid, mxid)
        sid=mxid+1
        _kw['id'] = '%s-%s' % (_kw['pid'],i)
        sub_taskids.append(_kw['id'])
        get_task_queue(w).push(_kw)
        i+=1
    kw['subtaskes']=sub_taskids
    get_task_list().__setitem__(_kw['pid'],kw)
    return json_dumps({"status":1,"info":sub_taskids})
    
    
def callback(kw):
    """
    任务完成后的回调函数
    合并返回结果
    """
    dbsource = get_conn_hash()
    output   = kw.get('output')
    pid      = kw.get('pid')
    res_queue= get_result_queue(pid)
    
    rs       = []
    for i in res_queue.__iter__():
        if i:
            rs.append(i)
    if not rs:
        return
    if len(rs) > 1:
        from utils import union_dict
        data = union_dict(*rs)
    else:
        data = rs[0]
    
    db       = dbclass(dbsource.get(output['dbserver'])['info'])
    kcount   = sum(data.values())
    db.connect()
    db.select_db(output['dbname'])
    sql = "insert into kw_illegal_log(kcount,taskid,contents)values('%s','%s','%s')" % \
                (kcount,pid,addslashes(json_dumps(data)))
    res, desc = db.query(sql,1)
    if res==0 and desc:
        rd=get_redis()
        rd.delete('wbsp:result.%s' % pid)
        