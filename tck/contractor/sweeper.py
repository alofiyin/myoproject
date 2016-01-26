#_*_coding:utf-8_*_

""" 处理任务完成后的善后工作

"""
from threading import Thread
import datetime
import time
from datamodel import *
from task_reg_model import task_registry
import sys, os
import logging
import traceback


logger = logging.getLogger('sweep')

def check_status(task):
    """检查子任务状态
    """
    done_time=[]
    try:
        for stk in get_sub_hash().mget(task['subtaskes']):
            if stk['status'] not in [0,3]:
                return (task,stk['status'])
            done_time.append(stk['donetime'])
        task['donetime']=max(done_time)
    except:
        pass
    return (task,0)
    
def sweep_task(task,status):
    """清理函数 
    """
    if status in [0,3]:
        #如果有回调函数则调用
        func = task['pid'].split('-')[0]
        if  func+'_callback' in task_registry.keys():
            t = Thread(target=task_registry[func+'_callback'],args=(task,))
            t.setDaemon(True)
            t.start()
            
        subtask_rd  = get_sub_hash()
        subtask_hrd = get_sub_history_hash()
        for tid in task['subtaskes']:
            stk = subtask_rd.get(tid)
            if stk:
                subtask_rd.__delitem__(tid)
                subtask_hrd.set(tid,stk)

        get_task_hitory_list().set(task['pid'],task)
        get_task_list().__delitem__(task['pid'])
class SweeperThread(Thread):
    """ 清洁工线程 """
    def __init__(self):
        super(SweeperThread, self).__init__()

    def run(self):
    
        while True:
            try:
            
                for k,task in get_task_list().items():
                    #清理任务队列
                    sweep_task(*check_status(task))
    
            except Exception as e:
                errinfo = traceback.format_exc()
                logger.error(errinfo)
            time.sleep(10)


def start_sweeper():
    cron_thread = SweeperThread()
    cron_thread.setDaemon(True)
    sys.stdout.write("start sweeper Thread...\n")
    cron_thread.start()
