#!/usr/local/python3/bin/python3
#_*_coding:utf-8_*_

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#http service 
#$Id: server.py 649 2015-06-12 fiyin $#

import json 
import os, time, sys
import logging
import logging.config
import mysqlwrap
import rediswrap
import multiprocessing as mp
import zkwrap


from threading import Thread
try:
    from Queue import Queue
except:
    from queue import Queue
from system_info import get_ip

import setproctitle
from signal import signal, SIGINT, SIG_IGN,SIGTERM
#设置程序名
proc_title = "webapi"
setproctitle.setproctitle(proc_title)

sys.path.append("%s/%s" % (sys.path[0],'controllers'))
sys.path.append("%s/%s" % (sys.path[0],'modules'))
"""加载日志"""
logging.config.fileConfig('./conf/logging.conf')
logger = logging.getLogger('main')
#加载配置
import sconf

try:
    sconf.SYS = json.loads("".join(open('./conf/sys.json').read().split()))
except:
    print("Erro: the file sys.json  is not json format, please check!\n system exit..")
    os._exit(0)
try:
    sconf.HOST = json.loads("".join(open('./conf/host.json').read().split()))
    sconf.DATA_SOURC = json.loads("".join(open('./conf/databases.json').read().split()))
    #print(sconf.HOST)
    #print(sconf.DATA_SOURC)
except:
    pass
#加载业务配置文件
files = os.listdir("./conf")
for f in files:
    try:
        if f[:4]=='biz_' and f[-5:]=='.json':
            sconf.BIZ[f[4:-5]] = json.loads(open("./conf/%s"%f).read().replace('\n','').replace('\t',''))
    except:
        logger.error("config file %s not load.please check."%f)
#加载zk
zkwrap.setup('default',sconf.SYS['zk'])
#加载数据库
mysqlwrap.setup_db('default',sconf.SYS['mysql'])
mysqlwrap.pool_monitor()
#rediswrap.setup_redis('default',sconf.SYS['redis']['host'],sconf.SYS['redis']['port'])
rediswrap.setup_redis('cache',sconf.SYS['redis']['host'],sconf.SYS['redis']['port'],decode_flag=False)
sconf.SYS['root_dir'] = sys.path[0]


G_exit = False
mpexit = mp.Event()
#启动定时任务
#from stat_daemon import cron
#p = mp.Process(target=cron, args=(mpexit,))
#p.daemon = True
#p.start()


#信号处理
def sig_exit(a,b):
    mpexit.set()
	
    G_exit=True
    os._exit(0)
signal(SIGINT,sig_exit)
signal(SIGTERM,sig_exit)
#eventlet 与 multiprocessing冲突，所以要将eventlet
#放在最后加载
from pm_srvd import PMService
srvd = PMService()
srvd._port = 6000
srvd.listen()
"""
t = Thread(target= srvd.listen)
t.setDaemon(True)
t.start()
while True:
	if G_exit:
		mpexit.set()
		p.join()
		os._exit(0)
	time.sleep(1)
"""
