#_*_coding:utf-8_*_

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#http service 
#$Id: server.py 649 2015-06-12 fiyin $#

import json 
import os, time, sys
import logging
import logging.config
import ipswrap

try:
    from Queue import Queue
except:
    from queue import Queue
from system_info import get_ip
from pm_test import PMService
import setproctitle
from signal import signal, SIGINT, SIG_IGN
#设置程序名
proc_title = "stata-srvd"
setproctitle.setproctitle(proc_title)

sys.path.append("%s/%s" % (sys.path[0],'controllers'))
#加载配置
from modules import sconf
try:
    sconf.SYS = json.loads("".join(open('./conf/sys.json').read().split()))
except:
    print("Erro: the file sys.json  is not json format, please check!\n system exit..")
    os._exit(0)
sconf.SYS['root_dir'] = sys.path[0]
"""加载日志"""
logging.config.fileConfig('./conf/logging.conf')
logger = logging.getLogger('main')

G_exit = False


#信号处理
def sig_exit(a,b):
    G_exit=True
    os._exit(0)
signal(SIGINT,sig_exit)

srvd = PMService()
srvd._port = sconf.SYS['port']
srvd.listen()