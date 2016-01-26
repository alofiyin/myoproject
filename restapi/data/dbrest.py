#_*_coding:utf-8_*_
from cls_base import *
import sconf
from mysqlwrap import dbclass
from pprint import pprint
#
#数据接口
#
#----------------
#通用操作
#----------------

def  get_table_name(id,tableprefix):
	tid = int((id+1)/5000000)+1
	return "%s_%s" %(tableprefix,tid)   
        
def get_table_id(table,db=None):
	res,desc = db.query("select max(id) as mid from %s" % table)
	maxid       = desc[0]['mid'] + 1
	return maxid

  

def insert(kw):
	dbname		= kw.pop('dbname')
	table   	= kw.pop("table")
	#id          = int(kw.pop("id"))
	db          = get_dbhandle(dbname,flag=False)
	table 		= check_shard_table(db,dbname,table)
	res,des     = db.insert(table,kw)
	db.close()
	return res,des

def update(kw):
	dbname		= kw.pop('dbname')
	table   	= kw.pop("table")
	id          = int(kw.pop("id"))
	db          = get_dbhandle(dbname,flag=False)
	table 		= check_shard_table(db,dbname,table,id)
	#data        = kw.pop('data')
	
	res,des     = db.update(table,kw,"id=%s"%id) 
	db.close()
	return res,des  

def delete(kw):
	dbname		= kw.pop('dbname')
	table   	= kw.pop("table")
	id          = int(kw.pop("id"))
	if type(id) in (tuple,list):
		id			= ','.join(id)
	db          = get_dbhandle(dbname,flag=False)
	table = check_shard_table(db,dbname,table,id)
	sql         = "id in (%s)" % id
	res, des    = db.delete(table,sql)
	db.close()
	return res,des

def query(kw):
	dbname		= kw.pop('dbname')
	table   	= kw.get("table")
	db          = get_dbhandle(dbname)
	res, des    = db.query(kw)
	db.close()
	return res,des


def getbyid(kw):
	"""根据id串获取记录"""
	ids 			= kw.get('ids')
	if type(ids) in (tuple,list):
		ids			= ','.join(ids)
	data			= {}
	data['table']	= kw.get('table')
	data['dbname']	= kw.get('dbname')
	data['where'] 	= "id in(%s)" % ids
	data['fields']	= kw.get('fields','*')
	if type(data['fields']) in (tuple,list):
		data['fields'] = ','.join(data['fields'])	
	return query(data)

def getcount(kw):
	"""获取记录数"""
	data			= {}
	data['table']	= kw.get('table')
	data['dbname']	= kw.get('dbname')
	data['where'] 	= kw.get('where','')
	data['fields']	= 'count(0) as n'
	res, desc = query(data)
	if res == 0 and desc:
		desc = desc[0]['n']
	return res, desc
	
def getlist(kw):
	"""获取列表"""
	data			= {}
	data['table']	= kw.get('table')
	data['dbname']	= kw.get('dbname')
	data['where'] 	= kw.get('where','')
	data['fields']	= kw.get('fields','*')
	data['order']	= kw.get('order')
	data['ordertype']=kw.get('ordertype')
	page			= int(kw.get('page',1))
	pagesize		= int(kw.get('pagesize',sconf.PAGE_SIZE))
	#cursor			= int(kw.get('cursor',0))
	data['group']	= kw.get('group')	
	startnum		= pagesize * (page-1)
	where			= ''
	pagesite		= pagesize if pagesize < sconf.PAGE_SIZE_MAX else sconf.PAGE_SIZE_MAX
	if type(data['fields']) in (tuple,list):
		data['fields'] = ','.join(data['fields'])
	
	if data['order']:
		if type(data['order']) in (tuple,list):
			data['order'] = ','.join(data['order'])
		if data['ordertype']:
			data['order'] = "%s %s" % (data['order'],data['ordertype'])
	#if cursor:
	#	data['limit'] = pagesite
	#	where = "id>%s" % cursor
	#else:
	#	data['limit'] = "%s,%s" % (startnum,pagesite)
	data['limit'] = "%s,%s" % (startnum,pagesite)
	res, desc = query(data)
	#if res == 0 and desc and 'id' in data['fields']:
	#	cursor = desc[0]['id']
	return res, desc	
        
def check_shard_table(db,dbname,table,id=0):
	"""判断是表否分拆
		
	""" 
	dbinf = sconf.get_db_info(dbname,True)
	shard_table = dbinf['shard_table'].keys()
	if dbname in shard_table:
		if not id:
			id = get_table_id(tabe,db)
		table = get_table_name(id,tabe)    
	return table   
         
def get_dbhandle(dbname,flag=True):
	"""获取数据库操作句柄
		flag 只读标识 True选择数据库读库，False写库
	"""	
	dbinfo = sconf.get_db_info(dbname,flag)
	dbinfo['info']['dbname']=dbinfo['dbname']   
	db = dbclass(dbinfo['info'])
	res,desc = db.connect()
	if res == -1:
		return on_sql_error(desc)
	return db