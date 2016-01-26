#coding:utf-8

""" 有一个定时执行的list: ztq:list:cron

放进去的工作，会定期自动执行
"""
from threading import Thread
import datetime
import time,json
import datamodel
import sys, os
import logging
import task_reg_model
import traceback
import utils
logger = logging.getLogger('main.cron')

def has_cron(func,biz):
    """检查任务是否已存在
    """
    for cron in datamodel.get_cron_set():
        if cron['func'] == func and cron['biz'] == biz:
            return cron
    return False

def add_cron(cron_data):
    """ 添加定时任务 

    cron:{'func':任务函数名,
          'args':函数参数,
          'biz':业务号,
          'cron_info': ['0','0/5','*','*','*','*','*'] 定时内容 格式参详linux的crontable
    """
    cron_set = datamodel.get_cron_set()
    cron=has_cron(cron_data['func'],cron_data['biz'])
    if cron:
        cron_set.remove(cron)
    cron_set.add(cron_data)
    logger.info("cron add func[%s] biz[%s]" %(cron_data['func'],cron_data['biz']))

def remove_cron(func,biz):
    """移除定时任务
    """
    cron_set = datamodel.get_cron_set()
    for cron in cron_set:
        if cron['func'] == func and cron['biz'] == biz:
            cron_set.remove(cron)
    logger.info("cron remove func[%s] biz[%s]" %(func,biz))
    
def check_time(now,tag):
    """检查时间是否到期
    """
    if tag == '*':
        return True
    elif ',' in tag:
        tm = tag.split(',')
        if now in map(int,tm):
            return True
    elif '-' in tag:
        tm = list(map(int,tag.split('-')))
        tm = range(tm[0],tm[1])
        if now in tm:
            return True
    elif '/' in tag:
        tm = list(map(int,tag.split('/')))
        if now >= tm[0] and (now-tm[0])%tm[1] ==0 :
            return True
    else:
        if now == int(tag):
            return True
    return False


def check_cron_info(cron_info):
    """检查定时执行信息是否满足条件
        cron_info信息格式:['0','0/5','*','*','*','*'] 秒，分，时，日，月，周
        
    """
        
    time_now = time.localtime()
    now = [time_now.tm_sec,time_now.tm_min,time_now.tm_hour,time_now.tm_mday,time_now.tm_mon,time_now.tm_wday]
    for i in range(0,len(cron_info)):
        if not check_time(now[i],cron_info[i]):
            return False
    return True    
    
class CronThread(Thread):
    """ 定时检查cron列表，如果满足时间条件，放入相关的队列 """
    def __init__(self):
        super(CronThread, self).__init__()

    def run(self):
        """
            获取cron_info信息格式:['0','0/5','*','*','*','*','*']
        """
        
        
        while True:
            # 遍历cron列表检查并检查定时执行信息
            cron_set = datamodel.get_cron_set()
            try:
                if int(time.time())%86400==57600:
                    datamodel.clean_history()
                for cron in cron_set:
                    try:
                        if check_cron_info(cron['cron_info']):
                            if cron['func'] in task_reg_model.task_registry:
                                taskid = "%s-%s-%s" % (cron['func'],time.strftime('%Y%m%d'),int(time.time()))
                                cron['args']['pid'] = taskid
                                cron['args']['func']=cron['func']
                                task_reg_model.task_registry[cron['func']]((),**cron['args'])
                                logger.info(" exec func[%s] biz[%s]" % (cron['func'],cron['biz']))
                            else:
                                logger.error(" exec func[%s] biz[%s] no task  registry " % (cron['func'],cron['biz']))
                    except Exception as e:
                        errinfo = traceback.format_exc()
                        logging.getLogger('main').error(errinfo)
            except:
                pass       

            time.sleep(1)




def start_cron():
    cron_thread = CronThread()
    cron_thread.setDaemon(True)
    logging.getLogger('main').info("start cron Thread...")
    cron_thread.start()
    return cron_thread
