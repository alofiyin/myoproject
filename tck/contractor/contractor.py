#_*_coding:utf-8_*_

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#工头主程序
#$Id: worker.py 649 2015-06-12 fiyin $#

import config 
from rediswrap import *
import os, time
import logging
import logging.config
from sweeper import start_sweeper
from cronthread import start_cron

try:
    from Queue import Queue
except:
    from queue import Queue
from system_info import get_ip
from contractor_servic import WEBServic

from signal import signal, SIGINT, SIG_IGN

"""初始化配置"""
logging.config.fileConfig('./conf/logging.conf')
logger = logging.getLogger('main')
config.read('./conf/worker.conf')
G_exit = False
SERVER = config.CONFIG['server']  #配置文件信息

#信号处理
def sig_exit(a,b):
    G_exit=True
    os._exit(0)
signal(SIGINT,sig_exit)


#注册redis消息中枢
setup_redis('default',SERVER['host'],int(SERVER['port']),SERVER['db'])
#启动清理工
start_sweeper()
#启动定时任务线程
start_cron()
srvd = WEBServic()
srvd.listen()