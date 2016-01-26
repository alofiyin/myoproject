#_*_coding:utf-8_*_
import falcon
from cls_base import cache_get,cache_set,get_cnf_val
import gzip,json,time
from pprint import pprint
import sconf
from hashlib import md5
from utils import JSONEncoder
import logging
from myapp import app
import dbrest as	dbhandle

logger = logging.getLogger('main')
#版本号
__Version = "1.0"

class comcorp:
	"""公司表相关查询
	"""
	def __init__(self):
		self.dbname = 'com'
		self.table	= 'com_corp'
	
	def on_get(self,req,resp,action):
		params		= req.params
		kw			= {}
		kw['table']	= self.table
		kw['dbname']= self.dbname
		kw['fields']= params.get('fields','')
		if action == 'getbyname':
			"""根据公司名称获取对应的信息"""
			com_name		= params.get('com_name','')
			if not com_name :
				raise falcon.HTTPBadRequest('illegal_argument','com_name must provided')
			kw['where']		= "com_name='%s'" % com_name
			result			= dbhandle.getlist(kw)
		
		elif action == 'getbydomain':	
			"""根据公司三级域名获取对应的信息"""	
			domain			= params.get('domain','')
			if not domain :
				raise falcon.HTTPBadRequest('illegal_argument','domain must provided')
			kw['where']		= "domain='%s'" % domain
			result			= dbhandle.getlist(kw)
		
		elif action == 'getmaxid':	
			"""获取公司的最大ID"""	
			kw['fields']	= 'max(id) as mx'
			result			= dbhandle.query(kw)
			if result[0] == 0:
				mx		= result[1][0]['mx']
				result	= 0,mx
		elif action == 'getlistbyuserid':	
			"""根据用户id获取公司的信息(多条信息)"""	
			user_id			= params.get('user_id','')
			if not user_id :
				raise falcon.HTTPBadRequest('illegal_argument','user_id must provided')
			kw['where']		= "user_id=%s" % user_id
			result			= dbhandle.getlist(kw)
			
		elif action == 'getbyuserid':	
			"""根据用户id获取公司的信息(单条信息)"""	
			user_id			= params.get('user_id','')
			if not user_id :
				raise falcon.HTTPBadRequest('illegal_argument','user_id must provided')
			kw['where']		= "user_id=%s" % user_id
			kw['limit']		= "1"
			result			= dbhandle.getlist(kw)
		elif action == 'gettagbycomid':
			"""根据公司id获取一条公司标签关联值"""
			kw['table']		= 'com_tag_relate'
			com_id			= params.get('com_id','')
			if not com_id :
				raise falcon.HTTPBadRequest('illegal_argument','com_id must provided')
			kw['where']		= "com_id=%s" % com_id	
			kw['limit']		= "1"	
			result			= dbhandle.getlist(kw)	
		elif action == 'getkeywbycomid':
			"""根据公司id获取公司展厅关键字"""
			kw['table']		= 'com_keyword'
			com_id			= params.get('com_id','')
			if not com_id :
				raise falcon.HTTPBadRequest('illegal_argument','com_id must provided')
			kw['where']		= "com_id=%s" % com_id	
			kw['limit']		= "1"	
			result			= dbhandle.getlist(kw)	
		else:
			raise falcon.HTTPError(falcon.HTTP_404,'invalid_grant','invalid action %s' % action)					
		if result[0] == -1:
			raise falcon.HTTPBadRequest('invalid_sql_syntax',str(result[1]))

		result={'result':result[1]}
		resp.body = JSONEncoder().encode(result)	
#--------
#注册模块路由
#--------

app.add_route('/%s/query/comcorp/{action}'% __Version,comcorp())