#_*_coding:utf-8_*_
from cls_base import *
from mysqlwrap import dbclass
from pprint import pprint
#
#数据接口-求购库
#
dbhostinfo = "base.mysql.biz72_buy"


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

