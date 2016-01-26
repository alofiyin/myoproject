#_*_coding:utf-8_*_
from cls_base import *
from mysqlwrap import dbclass
from pprint import pprint
#
#数据接口-产品库
#
dbhostinfo = "base.mysql.biz72_product"


def  getEditTableName(id,tableprefix):
		tid = (id+i)/5000000
		return "%s_%s" %(tableprefix,tid) 	

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
#数据库操作-产品表pro_info
#----------------	
@mysql(dbhostinfo)
def prod_insert(*args,**kw):
	db			= kw.pop("db")
	data		= kw.pop('data')
	res,desc 	= db.query("select max(id) as mid from pro_info")
	if res == -1: return err_handle.db_err
	maxid		= res[0]['mid'] + 1
	tableName 	= getEditTableName(maxid,'pro_info')
	res,des 	= db.insert(tableName,data)
	return res,des
	
@mysql(dbhostinfo)	
def prod_update(*args,**kw):
	db 			= kw.pop("db")
	data		= kw.pop('data')
	id 			= int(kw.pop("id"))
	tableName 	= getEditTableName(id,'pro_info')
	return db.update(tableName,data,"id=%s"%id)	
	
@mysql(dbhostinfo)	
def prod_delete(*args,**kw):
	db 			= kw.pop("db")
	id 			= int(kw.pop("id"))
	tableName 	= getEditTableName(id,'pro_info')
	sql			= "delete from %s where id=%s" % (tableName,id)
	return db.query(sql)
	
	