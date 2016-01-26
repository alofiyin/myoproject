#!/usr/local/python3/bin/python3
#_*_coding:utf-8_*_
import falcon
import json 
import os, time, sys
import logging
import logging.config
import mysqlwrap
import rediswrap
import route
import setproctitle
from wsgiref import simple_server

sys.path.append("%s/%s" % (sys.path[0],'controllers'))
sys.path.append("%s/%s" % (sys.path[0],'modules'))
sys.path.append("%s/%s" % (sys.path[0],'core'))
sys.path.append("%s/%s" % (sys.path[0],'data'))
"""加载日志"""
logging.config.fileConfig('./conf/logging.conf')
logger = logging.getLogger('main')
"""加载配置"""
import sconf
#设置配置文件目录
sconf.set_conf_path("%s/%s" % (sys.path[0],'conf'))
#加载系统配置
sconf.load_sys_conf()
#加载应用服务器配置
sconf.load_host_conf()
#加载数据源信息
sconf.load_db_conf()
#加载业务配置文件
sconf.load_biz_conf()
 
mysqlwrap.setup_db('default',sconf.SYS['mysql'])
mysqlwrap.pool_monitor()
#rediswrap.setup_redis('default',sconf.SYS['redis']['host'],sconf.SYS['redis']['port'])
rediswrap.setup_redis('cache',sconf.SYS['redis']['host'],sconf.SYS['redis']['port'],decode_flag=False)
sconf.SYS['root_dir'] = sys.path[0]

import myapp
app = application=myapp.app
#import ctl_bizcom
import ctl_dbo
import ctl_search
import ctl_bizcom
import ctl_bizprod
import ctl_bizuser
import ctl_bizhome
import ctl_bizzsinfo
import ctl_bizbuy
import ctl_biznews
#app.add_route('/test/{action}', test)
# 添加路由控制
swagger = sconf.swagger()
app.add_route('/swagger', swagger)
#r = route.route()
#for p,f in r.items():
#	print(p,f)
#	api.add_route(p, f)
#httpd = simple_server.make_server('0.0.0.0', 6000, app)
#httpd.serve_forever()
#gunicorn -w 8 -b 127.0.0.1:6000 app
#gunicorn -c gu.conf falcon_ap:app

import restapidoc
restapidoc.get_doc()
