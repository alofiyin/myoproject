#_*_coding:utf-8_*_
#后台运行的汇程序，定时查询redis中的累计项，根据
#stat_item_group表中sumdelay设定的时间阀值将数据
#入库

import stat_base
import sconf
import mysqlwrap
from sphinxwrap import sphinx
import rediswrap
import utils,json
import time
import logging
from threading import Thread
import multiprocessing as mp

RD_TMP_PRF = "stat:tmp:sum:"
logger = logging.getLogger('worker')
data_loge = logging.getLogger('dataerr')

def sumdelay():
	"""
	检测redis中的统计缓存，根据stat_item_group.sumdelay
	将满足条件的统计数据入库，并清除缓存
	"""
	rdb = rediswrap.get_redis()
	db = mysqlwrap.get_db()
	now = time.localtime()
	fields = rdb.keys(stat_base.RD_ITM_HST_TMP_PRFX+'*')

	if fields:
		gkeys = [f.split(':')[-1] for f in fields]

		todo_gkeys=[]
		step = 20
		#初始化时间
		clock = int(time.time())-120
		for i in range(0,len(gkeys),step):
			#每次提取step条group记录
			ks = ["'%s'" % k for k in gkeys[i:i+step]]
			sql = "select gkey,sumdelay,history_mrk from stat_item_group where gkey in (%s)" % ",".join(ks)
			res, desc = db.query(sql)
			if res==0 and desc:
				for row in desc:
					gk = ""
					#按时汇总
					if row['sumdelay'] == 2:
						clock = utils.timestamp(clock,'h')
						gk =row['gkey'] 
					#按天汇总，当前时间0点
					elif row['sumdelay'] == 1 and now.tm_hour==0:
						clock = utils.timestamp(0,'d')
						gk =row['gkey'] 
					#按月汇总，当天是1号，时间是0点
					elif row['sumdelay'] == 3 and (now.tm_mday==1 or now.tm_hour==0) :
						clock = utils.timestamp(0,'d')
						gk =row['gkey'] 
					#按周汇总,当天是周1，时间是0点
					elif row['sumdelay'] == 4 and (now.tm_wday!=1 or now.tm_hour!=0) :
						clock = utils.timestamp(0,'d')
						gk =row['gkey'] 
					#gk =row['gkey']
					if gk:
						#todo_gkeys.append(row)
						#print(stat_base.RD_ITM_HST_TMP_PRFX+row['gkey'],RD_TMP_PRF+row['gkey'])
						#rdb.rename(stat_base.RD_ITM_HST_TMP_PRFX+row['gkey'],RD_TMP_PRF+row['gkey'])

						key = stat_base.RD_ITM_HST_TMP_PRFX+gk
						r_item = rdb.hgetall(key)
						rdb.delete(key)
						tb = stat_base.get_hst_name(row['history_mrk'])
						cnt = 0
						if r_item:
							
							logger.info("sum stat group %s from %s into %s" % (row['gkey'],key,tb))
							ks = list(r_item.keys())
							#每次写50条记录
							for i in range(0,len(ks),50):
								value = ["('%s','%s','%s')" %(j,r_item[j],clock) for j in ks[i:i+50]]
								ins_sql = "insert into %s(itemid,val,clock)values%s" % (tb,','.join(value))
								res,desc = db.query(ins_sql,1)
								if res == -1:
									logger.error(str(desc))
									data_loge.info(ins_sql)
								else:
									cnt+=len(value)
							
							logger.info("[%s] count:[%s] ins:[%s] rows." %(gk,len(ks),cnt))
					
				#汇总数据入库
				"""
				for row in todo_gkeys:
					key = RD_TMP_PRF+row['gkey']
					r_item = rdb.hgetall(key)
					tb = stat_base.get_hst_name(row['history_mrk'])
					if r_item:
						loger.info("sum stat group %s from %s into %s" % (row['gkey'],key,tb))
						ks = list(r_item.keys())
						#每次写50条记录
						for i in range(0,len(ks),50):
							value = ["('%s','%s','%s')" %(j,r_item[j],clock) for j in ks[i:i+50]]
							res,desc = db.query("insert into %s(itemid,val,clock)values%s" % (tb,','.join(value)),1)
							if res == -1:
								logger.error(str(desc))
							print(res,desc)
				"""	
def cron(mpexit):
	import setproctitle
	proc_title = "stata-srvd cron mp"
	setproctitle.setproctitle(proc_title)
	while True:

		if  mpexit.is_set():
			print('mp exit....')
			break
		now = time.localtime()
		if now.tm_sec == 0 and now.tm_min==0:
			logger.info("sumdelay start.")
			try:
				sumdelay()
			except Exception as e:
				logger.info(str(e))
			logger.info("sumdelay end.")
		time.sleep(1)
										
if __name__=="__main__":

	import json
	sconf.SYS = json.loads("".join(open('../conf/sys.json').read().split()))
	sconf.HOST = json.loads("".join(open('../conf/host.json').read().split()))

	sconf.DATA_SOURC = json.loads("".join(open('../conf/databases.json').read().split()))
	#biz_info = json.loads("".join(open('../conf/biz.json').read().split()))
	biz_info = json.loads(open('../conf/biz.json').read().replace('\n','').replace('\t',''))

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
	
	