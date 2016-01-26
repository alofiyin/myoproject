#_*_coding:utf-8_*_
import gzip
import json
import time
from pprint import pprint
import logging
from sphinxwrap import sphinx
import sconf
from cls_base import *
import biz72_company
import biz_tag as tagsclass

myaction = {}
#---------------
#数据接口
#---------------
#公司表
@callback(myaction)
def cominsert(prama):
	"""插入一条公司记录
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int insertid] 
	Raises:
			[int errcode,string errinfo]
	"""
	return biz72_company.corp_insert(prama)

@callback(myaction)	
def cominfobyid(prama):
	"""根据id取公司记录
	Args:
		prama: dict type
			id: string type 
				example: "1,2,3 ....."
			fields: string type table's fields  default "id,com_name"
				example: "id,field1,field2,..." 
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]
	"""
	fields	= prama.get('fields','id,com_name')
	id		= prama.get('id','')
	if not id :
		return -6,"parameter id not set."
	kw		={}
	kw['table'] = 'com_corp'
	kw['fields'] = fields
	kw['where'] = 'id in (%s)' % id
	return biz72_company.query(kw)

@callback(myaction)	
def cominfobyname(prama):
	"""根据公司名称取公司相关信息
	Args:
		prama: dict type
			com_name: string type 
				example: "东莞市兆军电子有限公司"
			fields: string type table's fields  default "id,com_name,domain"
				example: "id,field1,field2,..." 
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]
	"""
	kw={}
	fields 			= prama.get('fields','id,com_name,domain')
	name			= prama.get('com_name','')
	if not name :
		return -6,"parameter com_name not set."
	kw['table'] 	= 'com_corp'
	kw['fields'] 	= fields
	kw['where'] 	= "com_name='%s'" % name
	res,cominfo		=biz72_company.query(kw)
	if res == 0 and cominfo:
		desc = []
		desc.append(cominfo[0])
		return desc
	return res,cominfo

@callback(myaction)	
def cominfobydomain(prama):
	"""根据公司三级域名获取对应的信息	
	Args:
		prama: dict type
			domain: string type 
				example: "gbmy783"
			fields: string type table's fields  default "id,com_name,domain"
				example: "id,field1,field2,..." 
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	fields 			= prama.get('fields','id,com_name,domain')
	domain			= prama.get('domain','')
	if not domain :
		return -6,"parameter domain not set."
	kw['table'] 	= 'com_corp'
	kw['fields'] 	= fields
	kw['where'] = "domain='%s'" % domain
	res,cominfo=biz72_company.query(kw)
	if res == 0 and cominfo:
		desc = []
		desc.append(cominfo[0])
		return desc
	return res,cominfo

@callback(myaction)	
def cominfobyuseridone(prama):
	"""根据用户id获取公司的信息(单条信息)
	Args:
		prama: dict type
			userid: int type 
			fields: string type table's fields  default "id,com_name,domain,user_id"
				example: "id,field1,field2,..." 
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]
	"""
	kw={}
	fields 			= prama.get('fields','id,com_name,domain,user_id')
	userid			= prama.get('userid',0)
	if not userid :
		return -6,"parameter userid not set."
	kw['table'] 	= 'com_corp'
	kw['fields'] 	= fields
	kw['where'] = "user_id=%s" % userid
	res,cominfo=biz72_company.query(kw)
	if res == 0 and cominfo:
		desc = []
		desc.append(cominfo[0])
		return desc
	return res,cominfo

@callback(myaction)	
def cominfobyuserid(prama):
	"""根据用户id获取公司的信息(多条信息)
	Args:
		prama: dict type
			userid: int type 
			fields: string type table's fields  default "id,com_name,domain,user_id"
				example: "id,field1,field2,..." 
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]
	"""
	kw={}
	fields 			= prama.get('fields','id,com_name,domain,user_id')
	userid			= prama.get('userid',0)
	if not userid :
		return -6,"parameter userid not set."
	kw['table'] 	= 'com_corp'
	kw['fields'] 	= fields
	kw['where'] = "user_id=%s" % userid
	return biz72_company.query(kw)

@callback(myaction)	
def commaxid(prama):
	"""获取公司的最大ID
	Args:
	Return:
		list type 
			[0, int maxid]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	fields 			= "max(id) as mid"
	if not userid :
		return -6,"parameter userid not set."
	kw['table'] 	= 'com_corp'
	kw['fields'] 	= fields
	res, desc = biz72_company.query(kw)
	if res == 0 and desc:
		return 0,desc[0]['mid']
	return res,desc
		
@callback(myaction)	
def comupdate(prama):
	"""更新一条公司记录
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"id:123,fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	return biz72_company.corp_update(prama)


@callback(myaction)		
def comdelete(prama):
	"""删除一条公司记录
	Args:
		prama: dict type
			id : int type  table's rowid
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	return biz72_company.corp_delete(prama)
#公司审核表
@callback(myaction)	
def checkinsert(prama):
	"""插入一条公司审核信息
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int insertid] 
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_corp_check'
	return biz72_company.insert(prama)

@callback(myaction)	
def checkupdate(prama):
	"""根据id更新一条公司审核信息
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"id:123,fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_corp_check'
	return biz72_company.update(prama)

@callback(myaction)		
def checkdelete(prama):
	"""删除一条审核信息
	Args:
		prama: dict type
			id : int type  table's rowid
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_corp_check'
	return biz72_company.delete(prama)

@callback(myaction)	
def checkinfobyid(prama):
	"""根据公司id获取一条审核信息
	Args:
		prama: dict type
			id: string type 
				example: "1,2,3 ....."
			fields: string type table's fields  default "*"
				example: "id,field1,field2,..." 
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	fields 			= prama.get('fields','*')
	comid			= prama.get('id',0)
	if not comid :
		return -6,"parameter id not set."
	kw['table'] 	= 'com_corp_check'
	kw['fields'] 	= fields
	kw['where'] = "id=%s" % comid
	return biz72_company.query(kw)

@callback(myaction)	
def checklist(prama):
	"""获取公司审核列表信息
	Args:
		prama: dict type
			page: int type default 1
			pageSize: int type default 20
			where: string type sql where syntax
				example:  "id=1 and status=1 ..."
			fields: string type table's fields  default "*"
			order: string type sql order by syntax
				example: "field desc/asc"
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	fields 			= prama.get('fields','*')
	page			= prama.get('page',1)
	pageSize		= prama.get('pageSize',20)
	startnum		= pageSize * (page-1)

	kw['table'] 	= 'com_corp_check'
	kw['fields'] 	= fields
	kw['order']		= prama.get('order','')
	kw['limit']		= "%s,%s" % (startnum,pageSize)
	return biz72_company.query(kw)

@callback(myaction)	
def checkcount(prama):
	"""获取公司审核列表数量
	Args:
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	kw['table'] 	= 'com_corp_check'
	kw['fields'] 	= "count(0) as num"
	res, desc =  biz72_company.query(kw)
	if res == 0 and desc:
		return 0, desc[0]['num']
	return res, desc

#标签关联值表
@callback(myaction)	
def taginsert(prama):
	"""插入公司标签关联值
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int insertid] 
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_tag_relate'
	return biz72_company.insert(prama)	
	
@callback(myaction)		
def tagupdate(prama):
	"""更新一条公司标签关联值
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"id:123,fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_tag_relate'
	return biz72_company.update(prama)

@callback(myaction)		
def tagdelete(prama):
	"""删除一条或者多条公司标签关联值
	Args:
		prama: dict type
			id : string type  table's rowids
				example: "1,2,3,..."
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_tag_relate'
	return biz72_company.delete(prama)
	
@callback(myaction)		
def taginfobyid(prama):
	"""根据id获取一条公司标签关联值
	Args:
		prama: dict type
			id: int type 
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	comid			= prama.get('id',0)
	if not comid :
		return -6,"parameter id not set."
	kw['table'] 	= 'com_tag_relate'
	kw['where'] = "id=%s" % comid
	return biz72_company.query(kw)

@callback(myaction)	
def taginfobycomid(prama):
	"""根据公司id获取一条公司标签关联值
	Args:
		prama: dict type
			comid: int type 
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]		
	"""
	kw={}
	comid			= prama.get('comid',0)
	if not comid :
		return -6,"parameter comid not set."
	kw['where'] = "com_id='%s'" % comid
	kw['table'] 	= 'com_tag_relate'
	res, desc = biz72_company.query(kw)	
	if res == 0 and desc:
		datainfo = []
		datainfo.append(desc[0])
		return 0,datainfo
	return res, desc
	
#公司展厅关键字表
@callback(myaction)	
def keywinsert(prama):
	"""插入公司展厅关键字
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int insertid] 
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_keyword'
	return biz72_company.insert(prama)	
@callback(myaction)		
def keywupdate(prama):
	"""更新一条公司展厅关键字
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"id:123,fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_keyword'
	return biz72_company.update(prama)

@callback(myaction)		
def keywdelete(prama):
	"""删除一条或者多条公司展厅关键字
	Args:
		prama: dict type
			id : string type  table's rowides
				example: "1,2,3,..."
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]	
	"""
	prama['table'] = 'com_keyword'
	return biz72_company.delete(prama)
	
@callback(myaction)		
def keywinfobyid(prama):
	"""根据id获取一条公司展厅关键字
	Args:
		prama: dict type
			userid: int type 
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	comid			= prama.get('id',0)
	if not comid :
		return -6,"parameter id not set."
	kw['table'] 	= 'com_keyword'
	kw['where'] = "id=%s" % comid
	return biz72_company.query(kw)

@callback(myaction)	
def keywinfobycomid(prama):
	"""根据公司id获取多条公司标签关联值
	Args:
		prama: dict type
			comid: int type 
			fields: string type table's fields  default "*"
				example: "id,field1,field2,..." 
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	fields 			= prama.get('fields','*')
	comid			= prama.get('comid',0)
	if not comid :
		return -6,"parameter comid not set."
	kw['fields']	= fields
	kw['where'] = "com_id='%s'" % comid
	kw['table'] 	= 'com_keyword'
	return biz72_company.query(kw)	

#公司相册表
@callback(myaction)	
def albuminsert(prama):
	"""插入公司相册类
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int insertid] 
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_photo_album'
	return biz72_company.insert(prama)	
	
@callback(myaction)		
def albumupdate(prama):
	"""更新一条公司相册类
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"id:123,fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_photo_album'
	return biz72_company.update(prama)

@callback(myaction)		
def albumdelete(prama):
	"""删除一条或者多条公司相册表信息
	Args:
		prama: dict type
			id : string type  table's rowides
				example: "1,2,3,..."
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_photo_album'
	return biz72_company.delete(prama)
	
@callback(myaction)		
def albuminfobyid(prama):
	"""根据id获取一条公司相册表信息
	Args:
		prama: dict type
			id: int type 
			fields: string type table's fields  default "*"
				example: "id,field1,field2,..." 
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	comid			= prama.get('id',0)
	if not comid :
		return -6,"parameter id not set."
	kw['table'] 	= 'com_photo_album'
	kw['where'] = "id=%s" % comid
	return biz72_company.query(kw)

@callback(myaction)	
def albumlistbycomid(prama):
	"""获取公司相册列表信息-分页
	Args:
		prama: dict type
			comid: int type
			page: int type default 1
			pageSize: int type default 20
			fields: string type table's fields  default "*"
			order: string type sql order by syntax
				example: "field desc/asc"
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	comid			= prama.get('comid',0)
	if not comid :
		return -6,"parameter id not set."
	fields 			= prama.get('fields','*')
	page			= prama.get('page',1)
	pageSize		= prama.get('pageSize',20)
	startnum		= pageSize * (page-1)
	kw['fields']	= fields
	kw['table'] 	= 'com_photo_album'
	kw['order']		= prama.get('order','')
	kw['where']		= 'com_id=%s' % comid
	kw['limit']		= "%s,%s" % (startnum,pageSize)
	return biz72_company.query(kw)	
		
@callback(myaction)	
def albumcount(prama):
	"""获取公司相册列表数量
	Args:
		prama: dict type
			comid : int type  
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	comid			= prama.get('comid',0)
	if not comid :
		return -6,"parameter comid not set."
	kw['table'] 	= 'com_photo_album'
	kw['fields'] 	= "count(0) as num"
	kw['where']		= 'com_id=%s' % comid
	res, desc =  biz72_company.query(kw)
	if res == 0 and desc:
		return 0, desc[0]['num']
	return res, desc

#公司图片表
@callback(myaction)	
def photosinsert(prama):
	"""插入公司图片
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int insertid] 
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_photos'
	return biz72_company.insert(prama)	
@callback(myaction)		
def photosupdate(prama):
	"""更新一条公司图片
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"id:123,fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_photos'
	return biz72_company.update(prama)

@callback(myaction)		
def photosdelete(prama):
	"""删除一条或者多条公司图片
	Args:
		prama: dict type
			id : string type  table's rowides
				example: "1,2,3,..."
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_photos'
	return biz72_company.delete(prama)
	
@callback(myaction)		
def photosinfobyid(prama):
	"""根据id获取一条公司图片
	Args:
		prama: dict type
			id: int type 
			fields: string type table's fields  default "*"
				example: "id,field1,field2,..." 
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	comid			= prama.get('id',0)
	if not comid :
		return -6,"parameter id not set."
	kw['table'] 	= 'com_photos'
	kw['where'] = "id=%s" % comid
	return biz72_company.query(kw)

@callback(myaction)	
def photoslistbycomid(prama):
	"""获取公司相册图片-分页
	Args:
		prama: dict type
			comid: int type
			albumid: int type
			page: int type default 1
			pageSize: int type default 20
			fields: string type table's fields  default "*"
			order: string type sql order by syntax
				example: "field desc/asc"
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	comid			= prama.get('comid',0)
	albumid		= prama.get('albumid','')
	if not comid :
		return -6,"parameter comid not set."
	fields 			= prama.get('fields','*')
	page			= prama.get('page',1)
	pageSize		= prama.get('pageSize',20)
	startnum		= pageSize * (page-1)
	kw['fields']	= fields
	kw['table'] 	= 'com_photos'
	kw['order']		= prama.get('order','')
	kw['where']		= 'com_id=%s' % comid
	if albumid :
		kw['where']+=' and album_id=%s' % albumid
	kw['limit']		= "%s,%s" % (startnum,pageSize)
	return biz72_company.query(kw)	
		
@callback(myaction)	
def photoscount(prama):
	"""获取公司相册图片数量
	Args:
		prama: dict type
			comid: int type
			albumid: int type
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]		
	
	"""
	comid			= prama.get('comid',0)
	albumid			= prama.get('albumid',0)
	if not comid :
		return -6,"parameter comid not set."	
	kw={}
	kw['table'] 	= 'com_photos'
	kw['fields'] 	= "count(0) as num"
	kw['where']		= 'com_id=%s' % comid
	if albumid :
		kw['where']+=' and album_id=%s' % albumid
	res, desc =  biz72_company.query(kw)
	if res == 0 and desc:
		return 0, desc[0]['num']
	return res, desc
			
#公司友情链接表信息	
@callback(myaction)	
def friendinsert(prama):
	"""插入公司友情链接表信息
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int insertid] 
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_friend_link'
	return biz72_company.insert(prama)	
	
@callback(myaction)		
def friendupdate(prama):
	"""根据id更新一条公司友情链接表信息
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"id:123,fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_friend_link'
	return biz72_company.update(prama)

@callback(myaction)		
def frienddelete(prama):
	"""删除一条或者多条公司友情链接表信息
	Args:
		prama: dict type
			id : string type  table's rowides
				example: "1,2,3,..."
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_friend_link'
	return biz72_company.delete(prama)
	
@callback(myaction)		
def friendinfobyid(prama):
	"""根据id获取一条公司友情链接表信息
	Args:
		prama: dict type
			id: int type 
			fields: string type table's fields  default "*"
				example: "id,field1,field2,..." 
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	comid			= prama.get('id',0)
	if not comid :
		return -6,"parameter id not set."
	kw['table'] 	= 'com_friend_link'
	kw['where'] = "id=%s" % comid
	return biz72_company.query(kw)

@callback(myaction)	
def friendlistbycomid(prama):
	"""获取公司友情链接列表信息-分页
	Args:
		prama: dict type
			comid: int type
			page: int type default 1
			pageSize: int type default 20
			fields: string type table's fields  default "*"
			order: string type sql order by syntax
				example: "field desc/asc"
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	comid			= prama.get('comid',0)
	if not comid :
		return -6,"parameter comid not set."
	fields 			= prama.get('fields','*')
	page			= prama.get('page',1)
	pageSize		= prama.get('pageSize',20)
	startnum		= pageSize * (page-1)

	kw['table'] 	= 'com_friend_link'
	kw['fields']	= fields
	kw['order']		= prama.get('order','')
	kw['where']		= 'com_id=%s' % comid
	kw['limit']		= "%s,%s" % (startnum,pageSize)
	return biz72_company.query(kw)	
		
@callback(myaction)	
def friendcount(prama):
	"""获取公司友情链接列表数量
	Args:
		prama: dict type
			comid: int type
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]		
	
	"""
	comid			= prama.get('comid',0)
	if not comid :
		return -6,"parameter comid not set."	
	kw={}
	kw['table'] 	= 'com_friend_link'
	kw['fields'] 	= "count(0) as num"
	kw['where']		= 'com_id=%s' % comid
	res, desc =  biz72_company.query(kw)
	if res == 0 and desc:
		return 0, desc[0]['num']
	return res, desc	

#公司动态
@callback(myaction)	
def newsinsert(prama):
	"""插入公司动态表信息
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int insertid] 
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_news'
	return biz72_company.insert(prama)	
	
@callback(myaction)		
def newsupdate(prama):
	"""根据id更新一条公司动态表信息
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"id:123,fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_news'
	return biz72_company.update(prama)

@callback(myaction)		
def newsdelete(prama):
	"""删除一条或者多条公司动态表信息
	Args:
		prama: dict type
			id : string type  table's rowides
				example: "1,2,3,..."
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_news'
	return biz72_company.delete(prama)
	
@callback(myaction)		
def newsinfobyid(prama):
	"""根据id获取一条公司动态表信息
	Args:
		prama: dict type
			id: int type 
			fields: string type table's fields  default "*"
				example: "id,field1,field2,..." 
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	comid			= prama.get('id',0)
	if not comid :
		return -6,"parameter id not set."
	kw['table'] 	= 'com_news'
	kw['where'] = "id=%s" % comid
	return biz72_company.query(kw)

@callback(myaction)	
def newslistbycomid(prama):
	"""获取公司动态列表信息-分页
	Args:
		prama: dict type
			comid: int type
			page: int type default 1
			pageSize: int type default 20
			fields: string type table's fields  default "id, com_id, title"
			where: string type sql where syntax
				example:  "id=1 and status=1 ..."
			order: string type sql order by syntax
				example: "field desc/asc"
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	comid			= prama.get('comid',0)
	if not comid :
		return -6,"parameter comid not set."
	fields 			= prama.get('fields','id, com_id, title')
	page			= prama.get('page',1)
	pageSize		= prama.get('pageSize',20)
	startnum		= pageSize * (page-1)
	where			= prama.get('where','')
	kw['table'] 	= 'com_news'
	kw['order']		= prama.get('order','')
	kw['fields']	= fields
	kw['where']		= 'com_id=%s' % comid
	if where : kw['where'] = "%s and %s" %(kw['where'],where)
	kw['limit']		= "%s,%s" % (startnum,pageSize)
	return biz72_company.query(kw)	
		
@callback(myaction)	
def newscount(prama):
	"""获取公司动态列表数量
	Args:
		prama: dict type
			comid: int type
			where: string type sql where syntax
				example:  "id=1 and status=1 ..."			
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]		
	
	"""
	comid			= prama.get('comid',0)
	where			= prama.get('where','')
	if not comid :
		return -6,"parameter comid not set."	
	kw={}
	kw['table'] 	= 'com_news'
	kw['fields'] 	= "count(0) as num"
	kw['where']		= 'com_id=%s' % comid
	if where : kw['where'] = "%s and %s" %(kw['where'],where)
	res, desc =  biz72_company.query(kw)
	if res == 0 and desc:
		return 0, desc[0]['num']
	return res, desc
		
#公司证书表
@callback(myaction)	
def certinsert(prama):
	"""插入公司证书
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int insertid] 
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_cert'
	return biz72_company.insert(prama)	
	
@callback(myaction)		
def certupdate(prama):
	"""根据id更新一条公司证书
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"id:123,fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_cert'
	return biz72_company.update(prama)

@callback(myaction)		
def certdelete(prama):
	"""删除一条或者多条公司证书信息
	Args:
		prama: dict type
			id : string type  table's rowides
				example: "1,2,3,..."
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_cert'
	return biz72_company.delete(prama)
	
@callback(myaction)		
def certinfobyid(prama):
	"""根据id获取一条公司证书表信息
	Args:
		prama: dict type
			id: int type 
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	comid			= prama.get('id',0)
	if not comid :
		return -6,"parameter id not set."
	kw['table'] 	= 'com_cert'
	kw['where'] = "id=%s" % comid
	return biz72_company.query(kw)

@callback(myaction)	
def certlistbycomid(prama):
	"""获取公司证书列表信息-分页
	Args:
		prama: dict type
			comid: int type
			page: int type default 1
			pageSize: int type default 20
			fields: string type table's fields  default "*"
			where: string type sql where syntax
				example:  "id=1 and status=1 ..."
			order: string type sql order by syntax
				example: "field desc/asc"
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	comid			= prama.get('comid',0)
	if not comid :
		return -6,"parameter comid not set."
	fields 			= prama.get('fields','*')
	page			= prama.get('page',1)
	pageSize		= prama.get('pageSize',20)
	startnum		= pageSize * (page-1)
	where			= prama.get('where','')
	kw['table'] 	= 'com_cert'
	kw['order']		= prama.get('order','')
	kw['fields']	= fields
	kw['where']		= 'com_id=%s' % comid
	if where : kw['where'] = "%s and %s" %(kw['where'],where)
	kw['limit']		= "%s,%s" % (startnum,pageSize)
	return biz72_company.query(kw)	
		
@callback(myaction)	
def certcount(prama):
	"""获取公司动证书表数量
	Args:
		prama: dict type
			comid: int type
			where: string type sql where syntax
				example:  "id=1 and status=1 ..."
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]		
	
	"""
	comid			= prama.get('comid',0)
	where			= prama.get('where','')
	if not comid :
		return -6,"parameter comid not set."	
	kw={}
	kw['table'] 	= 'com_cert'
	kw['fields'] 	= "count(0) as num"
	kw['where']		= 'com_id=%s' % comid
	if where : kw['where'] = "%s and %s" %(kw['where'],where)
	res, desc =  biz72_company.query(kw)
	if res == 0 and desc:
		return 0, desc[0]['num']
	return res, desc	

#公司黑名单表
@callback(myaction)	
def blackinsert(prama):
	"""插入公司黑名单
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int insertid] 
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_blacklist'
	return biz72_company.insert(prama)	
	
@callback(myaction)		
def blackupdate(prama):
	"""根据id更新一条公司黑名单
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"id:123,fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_blacklist'
	return biz72_company.update(prama)

@callback(myaction)		
def blackdelete(prama):
	"""删除一条或者多条公司黑名单信息
	Args:
		prama: dict type
			id : string type  table's rowides
				example: "1,2,3,..."
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_blacklist'
	return biz72_company.delete(prama)
	
@callback(myaction)		
def blackinfobyid(prama):
	"""根据id获取一条公司黑名单表信息
	Args:
		prama: dict type
			id: int type 
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	comid			= prama.get('id',0)
	if not comid :
		return -6,"parameter id not set."
	kw['table'] 	= 'com_blacklist'
	kw['where'] = "id=%s" % comid
	return biz72_company.query(kw)

@callback(myaction)	
def blacklist(prama):
	"""获取公司黑名单列表信息-分页
	Args:
		prama: dict type
			page: int type default 1
			pageSize: int type default 20
			fields: string type table's fields  default "*"
			where: string type sql where syntax
				example:  "id=1 and status=1 ..."
			order: string type sql order by syntax
				example: "field desc/asc"
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	fields 			= prama.get('fields','*')
	page			= prama.get('page',1)
	pageSize		= prama.get('pageSize',20)
	startnum		= pageSize * (page-1)
	where			= prama.get('where','')		
	kw['table'] 	= 'com_blacklist'
	kw['order']		= prama.get('order','')
	kw['fields']	= fields
	kw['where']		= where
	kw['limit']		= "%s,%s" % (startnum,pageSize)
	return biz72_company.query(kw)	
		
@callback(myaction)	
def blackcount(prama):
	"""获取公司动黑名单表数量
	Args:
		prama: dict type
			where: string type sql where syntax
				example:  "id=1 and status=1 ..."
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]		
	
	"""
	where			= prama.get('where','')
	kw={}
	kw['table'] 	= 'com_blacklist'
	kw['fields'] 	= "count(0) as num"
	kw['where']		= where
	res, desc =  biz72_company.query(kw)
	if res == 0 and desc:
		return 0, desc[0]['num']
	return res, desc	
	
#公司违法记录表
@callback(myaction)	
def illegalinsert(prama):
	"""插入公司违法记录
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int insertid] 
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_illegal_recode'
	return biz72_company.insert(prama)	
	
@callback(myaction)		
def illegalupdate(prama):
	"""根据id更新一条公司违法记录
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"id:123,fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_illegal_recode'
	return biz72_company.update(prama)

@callback(myaction)		
def illegaldelete(prama):
	"""删除一条或者多条公司违法记录信息
	Args:
		prama: dict type
			id : string type  table's rowides
				example: "1,2,3,..."
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_illegal_recode'
	return biz72_company.delete(prama)
	
@callback(myaction)		
def illegalinfobyid(prama):
	"""根据id获取一条公司违法记录表信息
	Args:
		prama: dict type
			id: int type 
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	comid			= prama.get('id',0)
	if not comid :
		return -6,"parameter id not set."
	kw['table'] 	= 'com_illegal_recode'
	kw['where'] = "id=%s" % comid
	return biz72_company.query(kw)

@callback(myaction)	
def illegallist(prama):
	"""获取公司违法记录列表信息-分页
	Args:
		prama: dict type
			page: int type default 1
			pageSize: int type default 20
			fields: string type table's fields  default "*"
			where: string type sql where syntax
				example:  "id=1 and status=1 ..."
			order: string type sql order by syntax
				example: "field desc/asc"
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	fields 			= prama.get('fields','*')
	page			= prama.get('page',1)
	pageSize		= prama.get('pageSize',20)
	startnum		= pageSize * (page-1)
	where			= prama.get('where','')		
	kw['table'] 	= 'com_illegal_recode'
	kw['order']		= prama.get('order','')
	kw['fields']	= fields
	kw['where']		= where
	kw['limit']		= "%s,%s" % (startnum,pageSize)
	return biz72_company.query(kw)	
		
@callback(myaction)	
def illegalcount(prama):
	"""获取公司动违法记录表数量
	Args:
		prama: dict type
			where: string type sql where syntax
				example:  "id=1 and status=1 ..."
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]		
	
	"""
	where			= prama.get('where','')
	kw={}
	kw['table'] 	= 'com_illegal_recode'
	kw['fields'] 	= "count(0) as num"
	kw['where']		= where
	res, desc =  biz72_company.query(kw)
	if res == 0 and desc:
		return 0, desc[0]['num']
	return res, desc		

#公司设置表
@callback(myaction)	
def settinginsert(prama):
	"""插入公司设置表信息
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int insertid] 
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_setting'
	return biz72_company.insert(prama)	
	
@callback(myaction)		
def settingupdate(prama):
	"""根据id更新一条公司设置表信息
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"id:123,fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_setting'
	return biz72_company.update(prama)

@callback(myaction)		
def settingdelete(prama):
	"""删除一条或者多条公司设置表信息
	Args:
		prama: dict type
			id : string type  table's rowides
				example: "1,2,3,..."
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_setting'
	return biz72_company.delete(prama)
	
@callback(myaction)		
def settinginfobyid(prama):
	"""根据id获取一条公司设置表信息
	Args:
		prama: dict type
			id: int type 
			fields: string type table's fields  default "*"
				example: "id,field1,field2,..." 
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	comid			= prama.get('id',0)
	if not comid :
		return -6,"parameter id not set."
	kw['table'] 	= 'com_setting'
	kw['where'] = "id=%s" % comid
	return biz72_company.query(kw)

@callback(myaction)	
def settinglistbycomid(prama):
	"""获取公司设置列表信息-分页
	Args:
		prama: dict type
			comid: int type
			page: int type default 1
			pageSize: int type default 20
			fields: string type table's fields  default "*"
			where: string type sql where syntax
				example:  "id=1 and status=1 ..."
			order: string type sql order by syntax
				example: "field desc/asc"
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	comid			= prama.get('comid',0)
	if not comid :
		return -6,"parameter comid not set."
	fields 			= prama.get('fields','*')
	page			= prama.get('page',1)
	pageSize		= prama.get('pageSize',20)
	startnum		= pageSize * (page-1)
	where			= prama.get('where','')
	kw['table'] 	= 'com_setting'
	kw['order']		= prama.get('order','')
	kw['fields']	= fields
	kw['where']		= 'com_id=%s' % comid
	if where : kw['where'] = "%s and %s" %(kw['where'],where)
	kw['limit']		= "%s,%s" % (startnum,pageSize)
	return biz72_company.query(kw)	
		
@callback(myaction)	
def settingcount(prama):
	"""获取公司设置列表数量
	Args:
		prama: dict type
			comid: int type
			where: string type sql where syntax
				example:  "id=1 and status=1 ..."
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]		
	
	"""
	comid			= prama.get('comid',0)
	where			= prama.get('where','')
	if not comid :
		return -6,"parameter comid not set."	
	kw={}
	kw['table'] 	= 'com_setting'
	kw['fields'] 	= "count(0) as num"
	kw['where']		= 'com_id=%s' % comid
	if where : kw['where'] = "%s and %s" %(kw['where'],where)
	res, desc =  biz72_company.query(kw)
	if res == 0 and desc:
		return 0, desc[0]['num']
	return res, desc	

#公司模版表
@callback(myaction)	
def tplinsert(prama):
	"""插入公司模版表信息
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int insertid] 
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_tpl'
	return biz72_company.insert(prama)	
	
@callback(myaction)		
def tplupdate(prama):
	"""根据id更新一条公司模版表信息
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"id:123,fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_tpl'
	return biz72_company.update(prama)

@callback(myaction)		
def tpldelete(prama):
	"""删除一条或者多条公司模版表信息
	Args:
		prama: dict type
			id : string type  table's rowides
				example: "1,2,3,..."
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_tpl'
	return biz72_company.delete(prama)
	
@callback(myaction)		
def tplinfobyid(prama):
	"""根据id获取一条公司模版表信息
	Args:
		prama: dict type
			id: int type 
			fields: string type table's fields  default "*"
				example: "id,field1,field2,..." 
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	comid			= prama.get('id',0)
	if not comid :
		return -6,"parameter id not set."
	kw['table'] 	= 'com_tpl'
	kw['where'] = "id=%s" % comid
	return biz72_company.query(kw)

@callback(myaction)	
def tpllist(prama):
	"""获取公司模版列表信息-分页
	Args:
		prama: dict type
			page: int type default 1
			pageSize: int type default 20
			fields: string type table's fields  default "*"
			where: string type sql where syntax
				example:  "id=1 and status=1 ..."
			order: string type sql order by syntax
				example: "field desc/asc"
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	fields 			= prama.get('fields','*')
	page			= prama.get('page',1)
	pageSize		= prama.get('pageSize',20)
	startnum		= pageSize * (page-1)
	where			= prama.get('where','')
	kw['table'] 	= 'com_tpl'
	kw['order']		= prama.get('order','')
	kw['fields']	= fields
	kw['where']		= where
	kw['limit']		= "%s,%s" % (startnum,pageSize)
	return biz72_company.query(kw)	
		
@callback(myaction)	
def tplcount(prama):
	"""获取公司模版列表数量
	Args:
		prama: dict type
			where: string type sql where syntax
				example:  "id=1 and status=1 ..."
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]		
	
	"""
	kw={}
	where			= prama.get('where','')
	kw['table'] 	= 'com_tpl'
	kw['fields'] 	= "count(0) as num"
	kw['where']		= where
	res, desc =  biz72_company.query(kw)
	if res == 0 and desc:
		return 0, desc[0]['num']
	return res, desc	

#公司模版标签表
@callback(myaction)	
def tpltaginsert(prama):
	"""插入公司模版标签表信息
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int insertid] 
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_tpl_tag'
	return biz72_company.insert(prama)	
	
@callback(myaction)		
def tpltagupdate(prama):
	"""根据id更新一条公司模版标签表信息
	Args:
		prama: dict type
			data : dict type  table's fields and values
				example: {"id:123,fieldname":"fieldvalue", ....}
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_tpl_tag'
	return biz72_company.update(prama)

@callback(myaction)		
def tpltagdelete(prama):
	"""删除一条或者多条公司模版标签表信息
	Args:
		prama: dict type
			id : string type  table's rowides
				example: "1,2,3,..."
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]
	"""
	prama['table'] = 'com_tpl_tag'
	return biz72_company.delete(prama)
	
@callback(myaction)		
def tpltaginfobyid(prama):
	"""根据id获取一条公司模版标签表信息
	Args:
		prama: dict type
			id: int type 
			fields: string type table's fields  default "*"
				example: "id,field1,field2,..." 
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	comid			= prama.get('id',0)
	if not comid :
		return -6,"parameter id not set."
	kw['table'] 	= 'com_tpl_tag'
	kw['where'] = "id=%s" % comid
	return biz72_company.query(kw)

@callback(myaction)	
def tptagllist(prama):
	"""获取公司模版标签列表信息-分页
	Args:
		prama: dict type
			page: int type default 1
			pageSize: int type default 20
			fields: string type table's fields  default "*"
			where: string type sql where syntax
				example:  "id=1 and status=1 ..."
			order: string type sql order by syntax
				example: "field desc/asc"
	Return:
		list type 
			[0, list datainfo]
			datainfo: table row data fetched 
				example:[{field1:value1,..},{field1,value1,...},...]
	Raises:
			[int errcode,string errinfo]	
	"""
	kw={}
	comid			= prama.get('comid',0)
	if not comid :
		return -6,"parameter comid not set."	
	fields 			= prama.get('fields','*')
	page			= prama.get('page',1)
	pageSize		= prama.get('pageSize',20)
	startnum		= pageSize * (page-1)
	where			= prama.get('where','')
	kw['table'] 	= 'com_tpl_tag'
	kw['order']		= prama.get('order','')
	kw['fields']	= fields
	kw['where']		= where
	kw['limit']		= "%s,%s" % (startnum,pageSize)
	return biz72_company.query(kw)	
		
@callback(myaction)	
def tpltagcount(prama):
	"""获取公司模版标签列表数量
	Args:
		prama: dict type
			where: string type sql where syntax
				example:  "id=1 and status=1 ..."
	Return:
		list type 
			[0, int rowcount]
	Raises:
			[int errcode,string errinfo]		
	
	"""
	kw={}
	where			= prama.get('where','')
	kw['table'] 	= 'com_tpl_tag'
	kw['fields'] 	= "count(0) as num"
	kw['where']		= where
	res, desc =  biz72_company.query(kw)
	if res == 0 and desc:
		return 0, desc[0]['num']
	return res, desc	
					
def search(kw):
	""" 获取搜索产品信息"""
	pass


#------------------------
#取得标签列表-从缓存取
#------------------------
def gettags(kw):
	"""标签缓存key: biz:prod:targ
	参数说明:
		bizcnf:业务配置信息
		tag_id:父标签
		lv2rows:二级标签提取数量
		lv3rows:三级标签提取数量
	"""
	#传入参数
	prama = kw.pop("prama",{})
	biznum = kw.get('biznum')
	#业务配置
	bizcnf = kw.pop("bizcnf")
	tag_id = str(prama.get('tag_id',bizcnf['prama']['tag_id']))
	tag_id_len = 0 if len(tag_id) < 3 else len(tag_id)
	lv2rows = prama.pop('lv2rows',bizcnf['prama']['lv2rows'])
	lv3rows = prama.pop('lv3rows',bizcnf['prama']['lv3rows'])

	res = cache_get("biz:targ.%s"%bizcnf['table'])
	if not res:
		s,res = tagsclass.prod_targs(biznum)
	else:
		res = json.loads(res)
	#组织数据
	#tag_id of level 1
	data={}
	if tag_id_len ==3 and tag_id in res and 'extn' in res[tag_id]:
		data = res[tag_id]
	elif tag_id_len ==6:
		data = res[str(tag_id)[:3]]['extn'][tag_id]
	#tag_id of all
	elif not tag_id or tag_id =='0':		
		data={'info':{'tag_id':0}}
		data['extn'] = res
	if data and 'extn' in data:
		res = tag_recursion(data,lv2rows,lv3rows)
		return 0,res 
	else:
		return 0,{}
	
def tag_recursion(data,n1=0,n2=0):
	"""递归组织标签
	参数说明:
	data 数据源 
		{"info":{"tag_id":"","total_num":"".....},
		"extn":{"info":{"tag_id":"","total_num":"".....},
				"extn":{"info":{"tag_id":"","total_num":"".....},
				}
			}
		}
	n1:二级标签提取数量
	n2:三级标签提取数量
	返回格式：
	{'info':{"tag_id":"","total_num":"".....},
	 'extn':[{'info':{"tag_id":"","total_num":"".....},
	 		'extn'{}...
	 		]
	 }
	"""
	
	res={'info':data['info']}
	if 'extn' not in data or not data['extn']:
		return res
	res['extn']=[]
	#排序
	sortList=[]
	for k,v in data['extn'].items():
		try:
			sortList.append([sum(json.loads(v['info']['total_num']).values()),k])
		except:
			if v['info']['total_num'] not in(0,'0'):
				sortList.append(row['info']['total_num'],k)				
	#sortList = [[sum(json.loads(k2['info']['total_num']).values()),k2['info']['tag_id']] for k2 in data['extn']]
	sortList.sort(reverse=True)
	tag_id = int(data['info']['tag_id'])
	n = n1 if tag_id >=100 and tag_id <1000 else n2
	if tag_id == 0:
		n = 0
	i=0
	for v,tid in sortList:
		if n and i==n:
			break
		i+=1
		if 'extn' in data['extn'][tid] and data['extn'][tid]['extn']:
			res['extn'].append(tag_recursion(data['extn'][tid],n1,n2))
		else:
			res['extn'].append(data['extn'][tid])
	return res
	
							
#------------------------
#根据标签取公司数据
#------------------------		
	
def list(kw):
	#传入参数
	prama = kw.pop("prama",{})
	biznum = kw.get('biznum')
	#业务配置
	bizcnf = kw.pop("bizcnf")
	#参数设置
	tag_id   = prama.get('tag_id',bizcnf['prama']['tag_id'])					
	pageSize = prama.get('pageSize',bizcnf['prama']['pageSize'])
	page     = prama.get('page',bizcnf['prama']['page'])
	kwords   = prama.get('kwords',"")
	fields   = prama.get('fields',bizcnf['prama']['fields'])
	#连接搜索引擎
	host_info = get_host_by_data(bizcnf['search']['source'])
	if  not host_info :
		return sconf.sphinx_index_not_found
	sp = sphinx(host_info['host'],host_info['port'])
	#搜索参数
	expression 				= bizcnf['search']['expression']
	expression['index'] 	= bizcnf['search']['source'].split('.')[-1]
	expression['pageSize']	= pageSize
	expression['page']		= page
	expression['keyw']		= kwords
	st = int(time.time())
	for tid in tag_id:
		tag_len = len(str(tid))
		if tag_len == 3:
			f = "r_com"
		elif tag_len == 6:
			f = "c_com"
		elif tag_len == 9:
			f = "com"
		#exp = expression.copy()
		expression['intType'][f]=str(tid)
		sp.initQuery(expression)
	rs = sp.RunQueries()
	#print("search_time:",time.time()-st)
	result = []
	st = int(time.time())
	if rs:
		#连接数据库
		dbinfo = get_host_by_data(bizcnf['data']['source'])
		dbinfo['dbname'] = bizcnf['data']['source'].split('.')[-1]
		db = dbclass(dbinfo)
		db.connect()
		for row in rs:
			sql_item =  bizcnf['data'].copy()
			sql_item['fields'] = fields
			ids = [str(k['id']) for k in row['matches']]
			print("ids:",ids)
			sql_item['where'] = sql_item['where'] % ",".join(ids)
			res,desc = db.query(sql_item)
			if res ==0 and desc:
				result.append(desc)
	else:
		result.append([])
	#print("search_time:",time.time()-st)
	#pprint(result)	
	#print(sp._error)
	return [0,result]
