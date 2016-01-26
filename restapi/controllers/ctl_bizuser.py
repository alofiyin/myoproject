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

class userinfo:
	"""用户表相关查询
	"""
	def __init__(self):
		self.dbname = 'user'
		self.table	= 'user_info'
	
	def on_get(self,req,resp,action):
		params		= req.params
		kw			= {}
		kw['table']	= self.table
		kw['dbname']= self.dbname
		kw['fields']= params.get('fields','')
		if action == 'getbyname':
			"""根据帐号获取一条用户帐号信息"""
			name		= params.get('name','')
			if not name :
				raise falcon.HTTPBadRequest('illegal_argument','name must provided')
			kw['where']		= "name='%s'" % name
			kw['order']		='id desc'
			result			= dbhandle.getlist(kw)
		
		elif action == 'getinfobyemail':	
			"""根据邮箱获取一条用户帐号信息"""	
			email			= params.get('email','')
			if not email :
				raise falcon.HTTPBadRequest('illegal_argument','email must provided')
			kw['where']		= "email='%s'" % email
			kw['order']		= 'id desc'
			res,desc		= dbhandle.getlist(kw)
			if res ==0 and desc:
				desc		= desc[0]
			result			= res,desc	
		else:
			raise falcon.HTTPError(falcon.HTTP_404,'invalid_grant','invalid action %s' % action)					
		if result[0] == -1:
			raise falcon.HTTPBadRequest('invalid_sql_syntax',str(result[1]))

		result={'result':result[1]}
		resp.body = JSONEncoder().encode(result)	
		
class usercorpfile:
	"""公司档案查询
	"""
	def __init__(self):
		self.dbname = 'user'
		self.table	= 'user_corp_file'
	
	def on_get(self,req,resp,action):
		params		= req.params
		kw			= {}
		kw['table']	= self.table
		kw['dbname']= self.dbname
		kw['fields']= params.get('fields','')
		if action == 'getcachebyuserid':
			"""根据会员ID获取公司档案缓存信息"""
			user_id		= params.get('user_id','')
			if not user_id :
				raise falcon.HTTPBadRequest('illegal_argument','user_id must provided')
			kw['where']		= "user_id=%s" % user_id
			kw['order']		='id desc'
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

app.add_route('/%s/query/userinfo/{action}'% __Version,userinfo())
app.add_route('/%s/query/usercorpfile/{action}'% __Version,usercorpfile())