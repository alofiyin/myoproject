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

class zsinfo:
	"""招商表相关查询
	"""
	def __init__(self):
		self.dbname = 'zhaoshang'
		self.table	= 'zs_info'
	
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
			"""获取公司招商列表数量"""	
			com_id			= params.get('com_id','')
			if not com_id :
				raise falcon.HTTPBadRequest('illegal_argument','com_id must provided')
			kw['page']		= params.get('page',1)
			kw['pagesize']	= params.get('pagesize',sconf.PAGE_SIZE)
			kw['order']		= params.get('order')
			kw['where']		= "com_id='%s'" % com_id
			result			= dbhandle.getlist(kw)
		
		elif action == 'getcount':	
			"""获取公司招商列表数量"""	
			com_id			= params.get('com_id','')
			if not com_id :
				raise falcon.HTTPBadRequest('illegal_argument','com_id must provided')
			kw['fields']	= 'count(id) as n'
			kw['where']		= "com_id='%s'" % com_id
			result			= dbhandle.query(kw)
			if result[0] == 0:
				n			= result[1][0]['n']
				result		= 0,n				

		else:
			raise falcon.HTTPError(falcon.HTTP_404,'invalid_grant','invalid action %s' % action)					
		if result[0] == -1:
			raise falcon.HTTPBadRequest('invalid_sql_syntax',str(result[1]))

		result={'result':result[1]}
		resp.body = JSONEncoder().encode(result)	
		
class zstag:
	"""标签表相关查询
	"""
	def __init__(self):
		self.dbname = 'zhaoshang'
		self.table	= 'zs_tag'
	
	def on_get(self,req,resp,action):
		params		= req.params
		kw			= {}
		kw['table']	= self.table
		kw['dbname']= self.dbname
		kw['fields']	= params.get('fields','id,name,tag_id,order_sort')
		if type(kw['fields']) in (tuple,list):
			kw['fields'] = ','.join(kw['fields'])
		if action == 'getroottag':
			"""获取一级标签信息"""
			kw['where']		= "tag_id<1000"
			res, desc		= dbhandle.query(kw)
			if res ==0:
				rs			= {}
				for row in desc:
					rs[row['tag_id']] = row
				result		= 0,rs
			else:
				result = res, desc
								
		elif action == 'getsecondtag':	
			"""获取二级标签信息"""	
			kw['where']		= "tag_id>1000 and tag_id <1000000"
			res, desc		= dbhandle.query(kw)
			if res ==0:
				rs			= {}
				for row in desc:
					rs[row['tag_id']] = row
				result		= 0,rs
			else:
				result = res, desc
				
		elif action == 'getsubtag':	
			"""获取一级标签的所有子类"""	
			tag_id			= int(params.get('tag_id',0))
			if not tag_id :
				raise falcon.HTTPBadRequest('illegal_argument','tag_id must provided')
			kw['where']		= "tag_id=%s or (tag_id>%s and tag_id <%s) or (tag_id>%s and tag_id <%s)" % (tag_id,(tag_id*100),((tag_id+1)*1000),(tag_id*1000000),((tag_id+1)*1000000))
			res, desc		= dbhandle.query(kw)
			if res ==0:
				rs			= {}
				for row in desc:
					rs[row['tag_id']] = row
				result		= 0,rs
			else:
				result = res, desc
				
		elif action == 'getcurrentsubtag':	
			"""获取当前标签的下一级分类
			"""	
			tag_id			= int(params.get('tag_id',0))
			if not tag_id:
				kw['where']	= 'tag_id<1000'
			else:
				kw['where']	= ' tag_id>%s and tag_id<%s'%((tag_id*100),((tag_id+1)*1000))
			res, desc		= dbhandle.query(kw)
			if res ==0:
				rs			= {}
				for row in desc:
					rs[row['tag_id']] = row
				result		= 0,rs
			else:
				result = res, desc
		elif action == 'getbytagid':	
			"""根据tag_id获取对应的标签信息
			"""	
			tag_id			= params.get('tag_id',0)
			if not tag_id :
				raise falcon.HTTPBadRequest('illegal_argument','tag_id must provided')
			if type(tag_id) in (tuple,list):
				tag_id = ','.join(tag_id)
			kw['where']	= 'tag_id in (%s)' % tag_id
			res, desc		= dbhandle.query(kw)
			if res ==0:
				rs			= {}
				for row in desc:
					rs[row['tag_id']] = row
				result		= 0,rs
			else:
				result = res, desc

		elif action == 'gettagbykeyw':	
			"""根据名称查找对应的标签信息
			"""	
			name			= params.get('name','')
			if not name :
				raise falcon.HTTPBadRequest('illegal_argument','name must provided')
			kw['where']	= "name='%s'" % name
			result			= dbhandle.query(kw)

		elif action == 'gettags':	
			"""获取所有标签信息
			"""		
			result			= dbhandle.query(kw)

		elif action == 'gettagsbynames':	
			"""根据标签名称列表获取产品标签ID
			"""	
			name			= params.get('name','')
			if not name :
				raise falcon.HTTPBadRequest('illegal_argument','name must provided')
			if type(name) in (tuple,list):
				name = ','.join(['"%s"'%k for k in name])
				kw['where']	= 'name in (%s)' % name
			else:
				kw['where']	= "name='%s'" % name
			result			= dbhandle.query(kw)

		else:
			raise falcon.HTTPError(falcon.HTTP_404,'invalid_grant','invalid action %s' % action)	
			
		if result[0] == -1:
			raise falcon.HTTPBadRequest('invalid_sql_syntax',str(result[1]))

		result={'result':result[1]}
		resp.body = JSONEncoder().encode(result)	
		
		

#--------
#注册模块路由
#--------

app.add_route('/%s/query/zsinfo/{action}'% __Version,zsinfo())
app.add_route('/%s/query/zstag/{action}'% __Version,zstag())
