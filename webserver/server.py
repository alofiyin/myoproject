#_*_coding:utf-8_*_

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#http service 
#$Id: server.py 649 2015-06-12 fiyin $#

import config 
import os, time, sys
import logging
import logging.config
import ipswrap

try:
    from Queue import Queue
except:
    from queue import Queue
from system_info import get_ip
from pm_srvd import PMService
import setproctitle
from signal import signal, SIGINT, SIG_IGN
#设置程序名
proc_title = "tools-srvd"
setproctitle.setproctitle(proc_title)

sys.path.append("%s/%s" % (sys.path[0],'modules'))
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

srvd = PMService()
srvd.listen()