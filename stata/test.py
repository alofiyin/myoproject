import json
import logging
import logging.config
import sys
import mysqlwrap
import rediswrap
sys.path.append("%s/%s" % (sys.path[0],'modules'))
from stat_daemon import sumdelay
import sconf
sconf.SYS = json.loads("".join(open('./conf/sys.json').read().split()))
sconf.HOST = json.loads("".join(open('./conf/host.json').read().split()))
logging.config.fileConfig('./conf/logging.conf')

sconf.DATA_SOURC = json.loads("".join(open('./conf/databases.json').read().split()))
#biz_info = json.loads("".join(open('../conf/biz.json').read().split()))
biz_info = json.loads(open('./conf/biz.json').read().replace('\n','').replace('\t',''))

#加载数据库
mysqlwrap.setup_db('default',sconf.SYS['mysql'])
mysqlwrap.pool_monitor()
rediswrap.setup_redis('default',sconf.SYS['redis']['host'],sconf.SYS['redis']['port'])

rdb = rediswrap.get_redis()
#res = rdb.scan(0,match='stat*',count=10 )
#res = rdb.keys('test*')
#print(help(rdb.rename))
#res = rdb.renamenx ('test:zset.1','test:rename.1')
#res = rdb.hgetall('stat:items:Crawler_stat.json' )
#res = rdb.hgetall('stat:hst:tmp:Crawler_stat.json' )
#print(res)
sumdelay()