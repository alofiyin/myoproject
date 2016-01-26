#_*_coding:utf-8_*_

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#通过redis做为消息中枢获取指令,监听指令队列
#$Id: command_redis.py 649 2015-06-08 fiyin $#
__author__ = 'fiyin <alofiyin@gmail.com>'
__version__ = '$Revision: 0.1 $'
import config 
from rediswrap import *
from datamodel import *
import utils
import jobs_reg_mode
import os, time
import logging
import traceback
from threading import Thread
import global_list

#SERVER_NAME = 'wbsp'
#WORKNAME_NAME = ''
#LOCAL_IP = get_ip()
#DOING_TASKES={}
#G_EXIT = False

logger = logging.getLogger('worker')
class JobRedisThread(Thread):
    def __init__(self,task_queue):
        super(JobRedisThread, self).__init__()
        self.task_queue = task_queue
        self.erro_queue = get_sys_err_queue()
            
    def run(self):
        task = None
        tasks = get_task_queue(global_list.WORKNAME_NAME)
        while True:
            if global_list.G_EXIT :
                break
            try:
                task = tasks.pop(timeout=5)
                if task :
                    self.task_queue.put(task)
            except Exception as e:
                errinfo = traceback.format_exc()
                _task = task or {'id':'','pid':'','args':'','keyword':''}
                _task['worker'] = global_list.WORKNAME_NAME
                _task['runtime'] = time.time()
                _task['errinfo'] = errinfo
                self.erro_queue.append(_task)
                time.sleep(3)
                #traceback.print_exc()
                logger.error(errinfo)