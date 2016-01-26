#_*_coding:utf-8_*_
import gzip
import json
import time
from pprint import pprint
import logging
from sphinxwrap import sphinx
import sconf
from cls_base import *
import biz72_product
import biz_tag as tagsclass
#
#数据接口-产品
#
#产品表
@callback(myaction)
def prodinsert(prama):
	"""插入一条产品记录
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
	return biz72_product.prod_insert(prama)

@callback(myaction)	
def prodinfobyid(prama):
	"""根据id取产品记录
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
	kw['table'] = 'com_prod'
	kw['fields'] = fields
	kw['where'] = 'id in (%s)' % id
	return biz72_product.query(kw)

@callback(myaction)	
def prodinfobycomid(prama):
	"""根据公司ID获取产品列表
	Args:
		prama: dict type
			comid: string type 
				example: "1,2,3,..."
			page: int type default 1
			pageSize: int type default 20
			fields: string type table's fields  default "id,com_name,com_id,title"
				example: "id,field1,field2,..." 
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
	fields 			= prama.get('fields','id,com_name,com_id,title')
	comid			= prama.get('comid','')
	where			= prama.get('where')
	order			= prama.get('order','')
	if not comid :	return -6,"parameter comid not set."
	kw['table'] 	= 'pro_info'
	kw['order']		= order
	kw['fields'] 	= fields
	kw['where'] 	= "com_name='%s'" % comid
	if where: kw['where'] = "%s and %s" %(kw['where'],where)
	return biz72_product.query(kw)

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
	kw['table'] 	= 'com_prod'
	kw['fields'] 	= fields
	kw['where'] = "domain='%s'" % domain
	res,cominfo=biz72_product.query(kw)
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
	kw['table'] 	= 'com_prod'
	kw['fields'] 	= fields
	kw['where'] = "user_id=%s" % userid
	res,cominfo=biz72_product.query(kw)
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
	kw['table'] 	= 'com_prod'
	kw['fields'] 	= fields
	kw['where'] = "user_id=%s" % userid
	return biz72_product.query(kw)

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
	kw['table'] 	= 'com_prod'
	kw['fields'] 	= fields
	res, desc = biz72_product.query(kw)
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
	return biz72_product.prod_update(prama)


@callback(myaction)		
def proddelete(prama):
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
	return biz72_product.prod_delete(prama)