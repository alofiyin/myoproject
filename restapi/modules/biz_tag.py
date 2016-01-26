#_*_coding:utf-8_*_
#统计系统基本操作函数集
from  sphinxwrap import sphinx
import json,time,gzip
import sconf
from mysqlwrap import dbclass
import cls_base 
import utils
from cls_base import get_host_by_data,get_cnf_val
from pprint import pprint

def prod_targs(key):
	"""产品标签"""
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
	rkey = "biz:targ.%s"%bizcnf['table']
	db = dbclass(dbinfo)
	res,desc = db.connect()
	
	if res == -1:
		return sconf.err_handle.db_err
	sql_item={}
	sql_item['table']	= bizcnf['table']
	sql_item['fields']	= bizcnf['fields']
	sql_item['order']	= "tag_id asc"

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
		cls_base.cache_set(rkey,json.dumps(obj),ttl)
		#except:
		#	pass
		return 0,obj

def addr_targs(key):
	"""省份城市标签"""
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
	prefix =  bizcnf['prefix']
	rkey = "biz:targ.%s.%s"%(bizcnf['table'],prefix)
	db = dbclass(dbinfo)
	res,desc = db.connect()
	
	if res == -1:
		return sconf.err_handle.db_err
	sql_item={}
	sql_item['table']	= bizcnf['table']
	sql_item['fields']	= bizcnf['fields']
	sql_item['order']	= "sortid asc"
	sql_item['where']	= " sortid >%s000 and sortid <%s999" % (prefix,prefix)
	res,desc1 = db.query(sql_item)
	sql_item['where']	= " sortid >%s000000 and sortid <%s999999" % (prefix,prefix)
	res,desc2 = db.query(sql_item)
	sql_item['where']	= " sortid >%s000000000 and sortid <%s999999999" % (prefix,prefix)
	res,desc3 = db.query(sql_item)
	
	if res == -1:
		return sconf.err_handle.db_err
	if desc:
		obj = {}
		for row in desc:
			tid = str(row['sortid'])
			if len(tid) ==3:
				obj[row['sortid']]={"info":row}
			elif len(tid) ==6:
				pid = int(tid[:3])
				if 'extn' not in  obj[pid]:
					obj[pid]['extn']={}
				obj[pid]['extn'][row['sortid']]={"info":row}
			elif len(tid)==9:

				ppid = int(tid[:3])
				pid =  int(tid[:6])
				if 'extn' not in  obj[ppid]['extn'][pid]:
					obj[ppid]['extn'][pid]['extn']={}
				obj[ppid]['extn'][pid]['extn'][row['sortid']]={"info":row}
		#try:
		#rdb.set(rkey,gzip.compress(json.dumps(res).encode()))
		cls_base.cache_set(rkey,json.dumps(obj),ttl)
		#except:
		#	pass
		return 0,obj
