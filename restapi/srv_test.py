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
import mysqlwrap
import rediswrap
import multiprocessing as mp
try:
    from Queue import Queue
except:
    from queue import Queue
from system_info import get_ip

import setproctitle
from signal import signal, SIGINT, SIG_IGN
#设置程序名
proc_title = "stata-srvd"
setproctitle.setproctitle(proc_title)

sys.path.append("%s/%s" % (sys.path[0],'controllers'))
sys.path.append("%s/%s" % (sys.path[0],'data'))
sys.path.append("%s/%s" % (sys.path[0],'modules'))
#加载配置
import sconf

try:
    sconf.SYS = json.loads("".join(open('./conf/sys.json').read().split()))
except:
    print("Erro: the file sys.json  is not json format, please check!\n system exit..")
    os._exit(0)
sconf.SYS['root_dir'] = sys.path[0]
"""加载日志"""
logging.config.fileConfig('./conf/logging.conf')
logger = logging.getLogger('main')
#加载配置

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

#加载数据库
mysqlwrap.setup_db('default',sconf.SYS['mysql'])
mysqlwrap.pool_monitor()
rediswrap.setup_redis('default',sconf.SYS['redis']['host'],sconf.SYS['redis']['port'])
rediswrap.setup_redis('cache',sconf.SYS['redis']['host'],sconf.SYS['redis']['port'])
sconf.SYS['root_dir'] = sys.path[0]
import cls_base
from  biz72_company import *

data = {"province": "101119", "domain": "", "con_fax": "\u00a0", "point": "0", "con_email": "", "con_web": "", "com_isoem": "0", "county": "101119101103", "com_jyms": "1", "con_name": "\u5362\u77eb\u5148\u751f  \uff08\u4e1a\u52a1\u7ecf\u7406\uff09", "com_mainway": "", "com_ppmc": "", "com_khyh": "", "topbaner": "", "com_cfmj": "", "city": "101119101", "pub_time": "1452033200", "user_id": "0", "com_khzh": "", "img": "", "com_ncke": "", "com_clsj": "0", "com_zczb": "", "com_enName": "", "com_mainpro": "", "com_zlkz": "", "com_frdb": "", "clk_times": "0", "status": "1", "update_time": "1452033200", "con_tel": "13535518362\u00a0", "mem_level": "0", "con_pv_num": "0", "com_zysc": "", "com_gsjj": "\u6b22\u8fce\u6765\u5230\u5e7f\u5dde\u68ee\u5ddd\u7535\u5b50\u79d1\u6280\u6709\u9650\u516c\u53f8\u5de5\u7a0b\u90e8\u7f51\u7ad9\uff0c \u5177\u4f53\u5730\u5740\u662f\u5e7f\u4e1c\u7701\u5e7f\u5dde\u5e02\u756a\u79ba\u533a\u756a\u79ba\u533a\u5927\u77f3\u9547\uff0c\u8054\u7cfb\u4eba\u662f\u5362\u77eb\u3002<br />\r\n\u8054\u7cfb\u7535\u8bdd\u662f34796177,\u8054\u7cfb\u624b\u673a\u662f13535518362,\u4e3b\u8981\u7ecf\u8425\u673a\u5e8a\u76f8\u5173\u4ea7\u54c1\u3002<br />\r\n\u5355\u4f4d\u6ce8\u518c\u8d44\u91d1\u672a\u77e5\u3002<br />\r\n\u6211\u4eec\u516c\u53f8\u4e3b\u8425\u673a\u5e8a \u91d1\u5c5e\u5236\u54c1 \u6cd5\u5170 \uff0c\u4e3a\u5ba2\u6237\u63d0\u4f9b\u597d\u7684\u4ea7\u54c1\u3001\u826f\u597d\u7684\u6280\u672f\u652f\u6301\u3001\u5065\u5168\u7684\u552e\u540e\u670d\u52a1\u4ee5\u53ca\u771f\u8bda\u7684\u6001\u5ea6\u5747\u5f97\u5230\u65b0\u8001\u5ba2\u6237\u7684\u4e00\u81f4\u597d\u8bc4\u3002\u516c\u53f8\u7ec4\u7ec7\u673a\u6784\u5065\u5168\u4e14\u62e5\u6709\u4e00\u6279\u7ecf\u9a8c\u4e30\u5bcc\u3001\u9ad8\u7d20\u8d28\u3001\u9ad8\u6548\u7387\u7684\u5458\u5de5\u961f\u4f0d\uff01\u672c\u516c\u53f8\u662f\u673a\u5e8a\u77e5\u540d\u4f01\u4e1a\uff0c\u516c\u53f8\u5b97\u65e8\uff1a\u7528\u6237\u81f3\u4e0a\uff0c\u8d28\u91cf\u7b2c\u4e00\uff0c\u4ee5\u8d28\u91cf\u6c42\u751f\u5b58\uff0c\u4ee5\u7528\u6237\u6548\u76ca\u6c42\u53d1\u5c55\uff0c\u4ea7\u54c1\u6280\u672f\u8ddf\u8e2a\u670d\u52a1\u3002\u6211\u4eec\u79c9\u6301\u201c\u4ee5\u5ba2\u6237\u4e3a\u5173\u6ce8\u7126\u70b9\u5e76\u8d85\u8d8a\u5ba2\u6237\u7684\u671f\u671b\u201d\u7684\u7ecf\u8425\u7406\u5ff5\uff0c\u672c\u7740\u8bda\u4fe1\u4e0e\u52a1\u5b9e\uff0c\u7aed\u8bda\u5730\u6b22\u8fce\u5168\u7403\u7684\u5ba2\u5546\u8385\u4e34\u60e0\u987e\uff0c\u540c\u8c0b\u53d1\u5c55\uff0c\u5171\u94f8\u8f89\u714c\uff01", "com_regadd": "", "com_ycl": "", "visualize": "", "con_ddr": "\u5e7f\u4e1c\u7701 \u5e7f\u5dde\u5e02 \u756a\u79ba\u533a \u756a\u79ba\u533a\u5927\u77f3\u9547", "com_njke": "", "com_gltx": "", "com_kind": "1", "con_code": "", "com_nyye": "", "con_qq": "", "country": "0", "class_tags": "\u6cd5\u5170", "com_ygrs": "", "con_phone": "34796177\u00a0", "com_jydd": "", "com_logo": "", "com_zykhq": "", "com_name": "\u5e7f\u5dde\u68ee\u5ddd\u7535\u5b50\u79d1\u6280\u6709\u9650\u516c\u53f8\u5de5\u7a0b\u90e8"}
#-------------
#测试数据库接口
kw={}
#---insert---
#kw['data']=data
#res,desc = corp_insert(kw)
#---update---
#data['id']=18944399
#data['com_name']='天津联胜合发金属制品有限公司'
#data['com_name']='广州森川电子科技有限公司'
#data['xxxx']=123
#kw['data']=data
#res,desc = corp_update(kw)
#print(res,desc)
#----del---
#data['id']=18944400
#kw['id']=18944403
#res,desc = corp_delete(kw)
#----query---
kw['data']={'where':'id=18944398','table':'com_corp'}
res,desc = query(kw)
print(res,desc)

