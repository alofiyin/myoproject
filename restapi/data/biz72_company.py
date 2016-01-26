#_*_coding:utf-8_*_
from cls_base import *
from mysqlwrap import dbclass
from pprint import pprint
#
#数据接口-产品库
#
dbhostinfo = "base.mysql.biz72_company"


def  getEditTableName(id,tableprefix):
		tid = int((id+1)/5000000)+1
		return "%s_%s" %(tableprefix,tid) 	

#----------------
#通用操作
#----------------
@mysql(dbhostinfo)
def insert(db,**kw):
	data		= kw.pop('data')
	tableName	= kw.pop("table")
	res,des 	= db.insert(tableName,data)
	return res,des
	
@mysql(dbhostinfo)	
def update(db,**kw):
	data		= kw.pop('data')
	id 			= int(data.pop("id"))
	tableName	= kw.pop("table")
	return db.update(tableName,data,"id=%s"%id)	
	
@mysql(dbhostinfo)	
def delete(db,**kw):
	id 			= int(kw.pop("id"))
	tableName 	= kw.pop("table")
	sql			= "id in (%s)" % id
	return db.delete(tableName,sql)
@mysql(dbhostinfo)
def query(db,**kw):
	return db.query(kw)
#----------------
#数据库操作-公司表com_corp
#----------------	
@mysql(dbhostinfo)
def corp_insert(db,**kw):
	data		= kw.pop('data')
	res,desc 	= db.query("select max(id) as mid from com_corp")
	if res == -1 :
		return err_handle.db_err
	maxid		= desc[0]['mid'] + 1
	tableName 	= getEditTableName(maxid,'com_corp')
	res,desc 	= db.insert(tableName,data)
	return res,desc
	
@mysql(dbhostinfo)	
def corp_update(db,**kw):
	data		= kw.pop('data')
	id 			= int(data.pop("id"))
	tableName 	= getEditTableName(id,'com_corp')
	return db.update(tableName,data,"id=%s"%id)	
	
@mysql(dbhostinfo)	
def corp_delete(db,**kw):
	id 			= int(kw.pop("id"))
	tableName 	= getEditTableName(id,'com_corp')
	sql			= "id=%s" % id
	return db.delete(tableName,sql)

