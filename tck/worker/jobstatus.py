#_*_coding:utf-8_*_

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#工作执行状态
#$Id: jobstatus.py 649 2015-06-24 fiyin $#
__author__ = 'fiyin <alofiyin@gmail.com>'
__version__ = '$Revision: 0.1 $'

from rediswrap import *
from datamodel import *
import global_list
import logging
import time

logger = logging.getLogger('worker.tasks')

def nothing(task):
    """干不了这个活
    """
    logger.error("[%s] not in jobs list!" % task['func'])
    task['status']=global_list.taskerr['notjob']
    get_sub_hash().set(task['id'],task)
        
def ready(task):
    """任务就绪
    """
    task['status'] = global_list.taskerr['doing']
    task['runtime'] = time.time()
    get_sub_hash().set(task['id'],task)        
    logger.info("%s [%s] is doing!" % (task['id'], task['func']))
    global_list.DOING_TASKES[task['id']]=task
    global_list.TASK_STAUS[task['id']]=0
def done(taskid):
    """完成任务
    """
    task = global_list.DOING_TASKES[taskid]
    logger.info("%s [%s] was done!" % (task['id'],task['func']))
    task['status'] = global_list.taskerr['done']
    task['donetime']=int(time.time())
    get_sub_hash().set(task['id'],task)
    global_list.DOING_TASKES.pop(taskid)
    global_list.TASK_STAUS.pop(taskid)
def doerror(taskid, err):
	"""任务出错
	"""
	task = global_list.DOING_TASKES[taskid]
	task['status'] = global_list.taskerr['runerr']
	task['donetime']=int(time.time())
	task['errinfo']= err
	get_sub_hash().set(task['id'],task)
	global_list.DOING_TASKES.pop(taskid)
	global_list.TASK_STAUS.pop(taskid)
