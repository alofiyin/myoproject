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

class buyinfo:
	"""求购表相关查询
	"""
	def __init__(self):
		self.dbname = 'buy'
		self.table	= 'buy_info'
	
	def on_get(self,req,resp,action):
		params		= req.params
		kw			= {}
		kw['table']	= self.table
		kw['dbname']= self.dbname
		kw['fields']= params.get('fields','')
		if action == 'getgroupbycomid':
			"""根据公司ID获取统计列表"""
			com_id		= params.get('com_id','')
			if not com_id :
				raise falcon.HTTPBadRequest('illegal_argument','com_id must provided')
			kw['group']		= params.get('group','status')
			kw['fields']	= '%s,count(id) as num' % kw['group']
			kw['order']		= 'NULL'
			kw['where']		= "com_id=%s" % com_id
			result			= dbhandle.getlist(kw)
		
		elif action == 'getlistbycomid':	
			"""获取公司求购列表数量"""	
			com_id			= params.get('com_id','')
			if not com_id :
				raise falcon.HTTPBadRequest('illegal_argument','com_id must provided')
			kw['page']		= params.get('page',1)
			kw['pagesize']	= params.get('pagesize',sconf.PAGE_SIZE)
			kw['order']		= params.get('order')
			kw['where']		= "com_id=%s" % com_id
			result			= dbhandle.getlist(kw)
		elif action == 'getcountbycomid':	
			"""根据公司ID获取产品列表数量"""	
			com_id			= params.get('com_id','')
			if not com_id :
				raise falcon.HTTPBadRequest('illegal_argument','com_id must provided')
			kw['fields']	= 'count(id) as n'
			kw['where']		= "com_id='%s'" % com_id
			result			= dbhandle.query(kw)
			if result[0] == 0:
				n			= result[1][0]['n']
				result		= 0,n				

		elif action == 'getlistbyname':	
			"""根据标题或标题+公司名称判断是否有重复值(多条信息)
			参数说明：	
				title 必须
				com_id 可选 
			返回值:
				status   不存在返回1,存在返回2
				data	 数据
			"""	
			com_id			= params.get('com_id','')
			title			= params.get('title','')
			if not title:
				raise falcon.HTTPBadRequest('illegal_argument','title must provided') 
			kw['where']		= "title='%s'" % title
			if com_id:
				kw['where'] = "com_id=%s and %s" % (com_id,kw['where'])
			res, desc		= dbhandle.getlist(kw)
			if res ==0:
				rs			= {'status':1,'data':[]}
				if desc  :
					rs['status'] = 2
					rs['data']	 = desc
				result		= 0,rs
			else:
				result = res, desc
		else:
			raise falcon.HTTPError(falcon.HTTP_404,'invalid_grant','invalid action %s' % action)	
							
		if result[0] == -1:
			raise falcon.HTTPBadRequest('invalid_sql_syntax',str(result[1]))

		result={'result':result[1]}
		resp.body = JSONEncoder().encode(result)	
		
		

#--------
#注册模块路由
#--------

app.add_route('/%s/query/buyinfo/{action}'% __Version,buyinfo())

