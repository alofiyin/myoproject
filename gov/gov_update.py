# -*- coding: utf-8 -*-
#Copyright  2015/8/21  fiyin
import mysqlwrap
import time
import datamodel
from threading import Thread
import traceback
import config 
import logging
from core import updata
import eventlet

import socket
eventlet.monkey_patch()
socket.setdefaulttimeout(10)

def doworke():
    db = mysqlwrap.get_db()
    sql_item = {}
    sql_item['table']= 'data_total'
    sql_item['fields']="id,gov_url"
    sql_item['where']=" isnull(reg_no)"
    sql_item['limit']=50
    sql_item['order']="id asc"
    id = 0
    pool     = eventlet.GreenPool(60)
    i=0
    while True:
        sql_item['where']+=" and id >%s" %id
        res,desc = db.query(sql_item)
        #print(res,desc)
        urls = []
        if res==0 and desc:
            for row in desc:
                urls.append(row['gov_url'])
                id = row['id']
            urls=[row['gov_url'] for row in desc ]
        if urls:
            for res in pool.imap(anhui.format_html,urls):
                i+=1
                if res and 'name' in res:
                    print("total_num:%s" % i,id)
                    print(updata(res,'ah'))
                else:
                    print(res) 

   
if __name__=="__main__":
    

    #dbinfo ={'host':'192.168.10.126','port':3306,'dbname':'gov_corp',
    #        'user':'wbsp','passwd':'wbsp','charset':'utf8'}

    #check_exist_corp('js')
    config.read('./conf/worker.conf')
    mysqlwrap.setup_db('default',config.CONFIG['mysqld'])
    THREAD_COUNT = 10
    import sys
    sys.path.append(sys.path[0]+'/modules')
    import anhui
    #rediswrap.setup_redis('default','192.168.10.126',6380)
    wk = Thread(target=doworke)
    wk.start()

    while True:

        time.sleep(3) 


