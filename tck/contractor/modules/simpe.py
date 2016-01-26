#_*_coding:utf-8_*_
# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#常归任务分配
#$Id: simpe.py 649 2015-08-24 fiyin $#
from rediswrap import *
from commands_ import *
import time, os
from datamodel import *

def run(f, **kw):

    #取得符合条件的worker
    workers = get_task_workers(job=f)
    if not workers:
        #raise Exception("no worker Standby!")
        return json_dumps({"status":-1,"info":"no worker Standby!"})
    #发布任务，（是否要根据workers的cup数来分配工作？）
    sub_taskids=[]
    w = workers[0]
    kw['id'] = '%s-%s' % (kw['pid'],1)
    sub_taskids.append(kw['id'])
    get_task_queue(w).push(kw)
    kw['subtaskes']=sub_taskids
    get_task_list().__setitem__(kw['pid'],kw)
    return json_dumps({"status":1,"info":sub_taskids})
    
