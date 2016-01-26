#_*_coding:utf-8_*_

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#执行任务
#$Id: jobexecute.py 649 2015-06-08 fiyin $#
__author__ = 'fiyin <alofiyin@gmail.com>'
__version__ = '$Revision: 0.1 $'

import jobs
import config 
import utils
import logging
import os, time,sys
import global_list
import jobs_reg_mode
import traceback
from jobstatus import *
from rediswrap import *
from datamodel import *
from threading import Thread

if sys.version >'3':
    from imp import reload
    
logger = logging.getLogger('worker.tasks')

class JobThread(Thread):

    def __init__(self,task_queue):
        super(JobThread, self).__init__()
        self.task_queue = task_queue
        self.reload_jobs_time = 100 
        self.sub_task_list = get_sub_hash()
        self.erro_queue = get_sys_err_queue()
            
    def close(self):
        """
           结束程序
        """    
        pass
    def reload_jobs(self):
        try:
            reload(jobs)
        except Exception as e:
            logger.error(str(e))
    
    def run(self):
        check_time = time.time()
        task = None
        
        while True:
            if global_list.G_EXIT :
                self.close()
                
            #定时重载jobs.py    
            #if  time.time() - check_time > self.reload_jobs_time:
            #    self.reload_jobs()
            
            #半阻塞式监听队列    
            try:
                try:
                    task = self.task_queue.get(timeout=5)                       
                except Exception as e:
                    task = None
                    
                #无任务继续
                if not task:
                    continue
                
                task['worker'] = global_list.WORKNAME_NAME
                #任务没在工作列表中  更新状态，放弃任务
                if task['func'] not in jobs_reg_mode.jobs_registry:
                    nothing(task['id'],task)
                    continue
                #更新任务状态就绪
                ready(task)
                #执行任务
                agrs = ()
                try:
                    jobs_reg_mode.jobs_registry[task['func']](*agrs, **task)
                    
                except Exception as e:
                    errinfo = traceback.format_exc()
                    logger.error("%s %s run err:%s" % (task['id'],task['func'],errinfo))
                    task['errinfo']=errinfo
                    task['status'] = global_list.taskerr['runerr']
                    self.sub_task_list.set(task['id'],task)
                    continue
                #任务完成
                #self.done(task)                   
            except Exception as e:
                #异常处理
                errinfo = traceback.format_exc()
                logger.error(errinfo)
                #traceback.print_exc()
                _task = task or {'id':'','pid':'','args':'','keyword':''}
                _task['worker'] = global_list.WORKNAME_NAME
                _task['runtime'] = time.time()
                _task['errinfo'] = errinfo
                if _task['id']: doerror(_task['id'], errinfo)
                self.erro_queue.append(_task)
                time.sleep(3)