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

class prodinfo:
	"""产品表相关查询
	"""
	def __init__(self):
		self.dbname = 'prod'
		self.table	= 'pro_info'
	
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
			"""根据公司ID获取产品列表"""	
			com_id			= params.get('com_id','')
			if not com_id :
				raise falcon.HTTPBadRequest('illegal_argument','com_id must provided')
			kw['page']		= params.get('page',1)
			kw['pagesize']	= params.get('pagesize',sconf.PAGE_SIZE)
			kw['order']		= params.get('order')
			kw['where']		= "com_id='%s'" % com_id
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
				rettype 返回信息类型,0返回数字,1返回重复的数据
			返回值:
				status   不存在返回1,存在返回2
				data	 数据
			"""	
			com_id			= params.get('com_id','')
			title			= params.get('title','')
			rettype			= int(params.get('rettype',0))
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
					if rettype==1:
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
		
class prodtag:
	"""标签表相关查询
	"""
	def __init__(self):
		self.dbname = 'prod'
		self.table	= 'pro_tag'
	
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
			"""获取标签信息(所有或者一级或者id名称对应信息)
	   			Args:
	   				tag_id		标签id
	  									0 显示所有标签
										1 显示一级标签,
	  									2 就显示二级标签,
									其它情况如:
	 									tag_id="101,102"显示tag_id=>名称对应的标签数组
			"""	
			tag_id			= params.get('tag_id','1')
			if tag_id in ['0','1','2']:
				tag_id = int(tag_id)
				if tag_id == 1:
					kw['where'] = "tag_id <1000"
				elif tag_id ==2:
					kw['where'] = "tag_id>1000 and tag_id <1000000"
			else:
				if type(tag_id) in (tuple,list):
					tag_id = ','.join(tag_id)	
				kw['where'] = "tag_id in (%s) " % tag_id			
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
		
class keywrelate:
	"""相关关键字查询
	"""
	def __init__(self):
		self.dbname = 'prod'
		self.table	= 'pro_relate_keyword'
	
	def on_get(self,req,resp,action):
		params		= req.params
		kw			= {}
		kw['table']	= self.table
		kw['dbname']= self.dbname
		kw['fields']	= params.get('fields','*')
		if type(kw['fields']) in (tuple,list):
			kw['fields'] = ','.join(kw['fields'])
		if action == 'getletter':
			"""根据字母字符串查找相关关键字"""
			letters			= params.get('letters','')
			if not letters :
				raise falcon.HTTPBadRequest('illegal_argument','letters must provided')
			kw['where']		= "letters='%s'" % letters 
			print(kw)
			result			= dbhandle.query(kw)
		
		elif action == 'getbyname':	
			"""根据关键字查找相关关键字(产品、公司、网址、求购)
			"""	
			keyw			= params.get('keyw','')
			if not keyw :
				raise falcon.HTTPBadRequest('illegal_argument','keyw must provided')
			kw['where']		= "keyw='%s'" % keyw
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

app.add_route('/%s/query/prodinfo/{action}'% __Version,prodinfo())
app.add_route('/%s/query/prodtag/{action}'% __Version,prodtag())
app.add_route('/%s/query/keywrelate/{action}'% __Version,keywrelate())