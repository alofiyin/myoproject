#_*_coding:utf-8_*_
from cls_base import *
from mysqlwrap import dbclass
from pprint import pprint
#
#数据接口-价格行情库
#
dbhostinfo = "base.mysql.biz72_price"


def  getEditTableName(id,tableprefix) {
		tid = (id+i)/5000000
		return "%s_%s" %(tableprefix,tid) 	

#----------------
#通用操作
#----------------
@cls_base.mysql(dbhostinfo)
def insert(*args,**kw):
	db			= kw.pop("db")
	data		= kw.pop('data')
	tableName	= kw.pop("table")
	res,des 	= db.insert(tableName,data)
	return res,des
	
@cls_base.mysql(dbhostinfo)	
def update(*args,**kw):
	db 			= kw.pop("db")
	data		= kw.pop('data')
	id 			= int(data.pop("id"))
	tableName	= kw.pop("table")
	return db.update(tableName,data,"id=%s"%id)	
	
@cls_base.mysql(dbhostinfo)	
def delete(*args,**kw):
	db 			= kw.pop("db")
	id 			= int(kw.pop("id"))
	tableName 	= kw.pop("table")
	sql			= "delete from %s where id=%s" % (tableName,id)
	return db.query(sql)

#----------------
#数据库操作-公司表com_corp
#----------------	
@cls_base.mysql(dbhostinfo)
def corp_insert(*args,**kw):
	db			= kw.pop("db")
	data		= kw.pop('data')
	res,desc 	= db.query("select max(id) as mid from price_info")
	if res == -1 return err_handle.db_err
	maxid		= res[0]['mid'] + 1
	tableName 	= getEditTableName(maxid,'price_info')
	res,des 	= db.insert(tableName,data)
	return res,des
	
@cls_base.mysql(dbhostinfo)	
def corp_update(*args,**kw):
	db 			= kw.pop("db")
	data		= kw.pop('data')
	id 			= int(kw.pop("id"))
	tableName 	= getEditTableName(id,'price_info')
	return db.update(tableName,data,"id=%s"%id)	
	
@cls_base.mysql(dbhostinfo)	
def corp_delete(*args,**kw):
	db 			= kw.pop("db")
	id 			= int(kw.pop("id"))
	tableName 	= getEditTableName(id,'price_info')
	sql			= "delete from %s where id=%s" % (tableName,id)
	return db.query(sql)
	
	