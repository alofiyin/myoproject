#_*_coding:utf-8_*_
#统计系统基本操作函数集
from  sphinxwrap import sphinx
import json,time,gzip
import sconf
from mysqlwrap import dbclass
import rediswrap 
import utils
from stat_base import get_host_by_data,get_cnf_val
from pprint import pprint

def prod_targs(key):
	bizcnf = get_cnf_val(key,sconf.BIZ)
	#取业务配置
	if not bizcnf:
		return sconf.err_handle.biznum_not_config
	ttl     = bizcnf.get('ttl',600)
	#取数据库配置
	dbinfo = get_host_by_data(bizcnf['source'])
	if not dbinfo:
		return sconf.err_handle.db_not_config
	dbinfo['dbname']=bizcnf['source'].split('.')[-1]
	rdb = rediswrap.get_redis('cache')
	rkey = "biz:targ.%s"%bizcnf['table']
	db = dbclass(dbinfo)
	res,desc = db.connect()
	
	if res == -1:
		return sconf.err_handle.db_err
	sql_item={}
	sql_item['table'] = bizcnf['table']
	sql_item['fields'] = bizcnf['fields']
	sql_item['order'] = "tag_id asc"

	res,desc = db.query(sql_item)

	if res == -1:
		return sconf.err_handle.db_err
	if desc:
		obj = {}
		for row in desc:
			tid = str(row['tag_id'])
			if len(tid) ==3:
				obj[row['tag_id']]={"info":row}
			elif len(tid) ==6:
				pid = int(tid[:3])
				if 'extn' not in  obj[pid]:
					obj[pid]['extn']={}
				obj[pid]['extn'][row['tag_id']]={"info":row}
			elif len(tid)==9:

				ppid = int(tid[:3])
				pid =  int(tid[:6])
				if 'extn' not in  obj[ppid]['extn'][pid]:
					obj[ppid]['extn'][pid]['extn']={}
				obj[ppid]['extn'][pid]['extn'][row['tag_id']]={"info":row}
		#try:
		#rdb.set(rkey,gzip.compress(json.dumps(res).encode()))
		rdb.set(rkey,json.dumps(obj))
		#except:
		#	pass
		return 0,obj