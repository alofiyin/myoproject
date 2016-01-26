#_*_coding:utf-8_*_

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#工人主程序 
#$Id: worker.py 649 2015-06-04 fiyin $#

import config 
from rediswrap import *
import os, time
import logging
import logging.config
import global_list
try:
    from Queue import Queue
except:
    from queue import Queue
from system_info import get_ip
from command_redis import CommandRedisThread
from commandexecute import CommandThread
from job_redis import JobRedisThread
from jobexecute import JobThread

from signal import signal, SIGINT, SIG_IGN,SIGTERM
"""初始化配置"""
logging.config.fileConfig('./conf/logging.conf')
logger = logging.getLogger('worker')
config.read('./conf/worker.conf')
#logger.info('test main logger')
global_list.SERVER_NAME = 'wbsp'    #服务名前缀
global_list.WORKNAME_NAME = ''      #工人编号
global_list.LOCAL_IP = get_ip()     #本机IP
global_list.PROC_POOL = {}          #线程列表
DOING_TASKES={}         #正在进行的任务列表
global_list.G_EXIT = False          #全局退出标记
SERVER = config.CONFIG['server']  #配置文件信息

#信号处理
def sig_exit(a,b):
    global_list.G_exit=True
    os._exit(0)
signal(SIGINT,sig_exit)
signal(SIGTERM,sig_exit)

#注册redis消息中枢
setup_redis('default',SERVER['host'],int(SERVER['port']),SERVER['db'])
#队列
cmd_queue = Queue(0)
task_queue = Queue(0)
#初始化命令执行线程

cmd_er = CommandThread(cmd_queue)
cmd_er.setDaemon(True)
cmd_er.start()
logger.info("start command thread.")
#启动消息中枢命令监听线程
cmd_rt = CommandRedisThread(cmd_queue)
cmd_rt.setDaemon(True)
cmd_rt.start()
logger.info("start command monitor thread.")
#任务监听线程
task_rt = JobRedisThread(task_queue)
task_rt.setDaemon(True)
task_rt.start()
#启动任务执行线程
task_et = JobThread(task_queue)
task_et.setDaemon(True)
task_et.start()

#启动命令执行线程

while True:
    #print("wating for ...",global_list.G_EXIT)
    if global_list.G_EXIT:
        print(" self exiting.....")
        os._exit(0)
    
    time.sleep(1)
    
        

    
    

					
                    

