#_*_coding:utf-8_*_

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#http service 
#$Id: server.py 649 2015-06-12 fiyin $#

import config 
import os, time, sys
import logging
import logging.config
import rediswrap
import mysqlwrap
import datamodel
import core
import setproctitle
from threading import Thread
try:
    from Queue import Queue
except:
    from queue import Queue
from system_info import get_ip
#from pm_srvd import PMService

from signal import signal, SIGINT, SIG_IGN,SIGTERM ,SIGCHLD

#设置程序名
setproctitle.setproctitle(datamodel.proc_title)

sys.path.append("%s/%s" % (sys.path[0],'modules'))
"""初始化配置"""
logging.config.fileConfig('./conf/logging.conf')
logger = logging.getLogger('main')
config.read('./conf/worker.conf')
G_exit = False
SERVER = config.CONFIG['server']  #配置文件信息


#信号处理
def sig_exit(a,b):
    print('sig:',a)
    logger.info("exit MainMnt..")
    datamodel.g_exit=True
    #os._exit(0)
signal(SIGINT,sig_exit)
signal(SIGTERM,sig_exit)
#signal(SIGCHLD,sig_exit)
#注册redis消息中枢
rediswrap.setup_redis('default',SERVER['host'],int(SERVER['port']),SERVER['db'])
logger.info("register redis.")
#注册数据库
mysqlwrap.setup_db('default',config.CONFIG['mysqld'])
#启动数据连接池守护进程
mysqlwrap.pool_monitor()
logger.info("register mysql.")
#启动数据源队列守护进程
qmnt = Thread(target=core.queue_mnt)
qmnt.setDaemon(True)
qmnt.start()
logger.info("start queue_mnt.")
#启动采集程序
logger.info("start MainMnt.")
core.MainMnt().run()
#srvd = PMService()
#srvd.listen()
os._exit(0)