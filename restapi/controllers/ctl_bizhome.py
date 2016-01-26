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

class common:
	"""获取省、市相关查询
	"""
	def __init__(self):
		self.dbname = 'home'
		self.table	= 'home_country_sort'
	
	def on_get(self,req,resp,action):
		params		= req.params
		kw			= {}
		kw['table']	= self.table
		kw['dbname']= self.dbname
		kw['fields']	= params.get('fields','id,name,sortid,letter')
		if type(kw['fields']) in (tuple,list):
			if 'sortid' not in kw['fields']:
				kw['fields'].append('sortid')
			kw['fields'] = ','.join(kw['fields'])
		if action == 'getroottag':
			"""获取一级标签信息"""
			kw['where']		= "sortid>101000 AND sortid<102000"
			res, desc		= dbhandle.query(kw)
			if res ==0:
				rs			= {}
				for row in desc:
					rs[row['sortid']] = row
				result		= 0,rs
			else:
				result = res, desc
								
		elif action == 'getsecondtag':	
			"""获取二级标签信息(城市)"""	
			kw['where']		= "sortid>101000000 AND sortid<102000000"
			res, desc		= dbhandle.query(kw)
			if res ==0:
				rs			= {}
				for row in desc:
					rs[row['sortid']] = row
				result		= 0,rs
			else:
				result = res, desc
				
				
		elif action == 'getrootsecondtag':	
			"""获取一、二级标签信息(省份、城市)
			"""	

			kw['where']	= '(sortid>101000 AND sortid<102000) OR (sortid>101000000 AND sortid<102000000)'
			res, desc		= dbhandle.query(kw)
			if res ==0:
				rs			= {}
				for row in desc:
					rs[row['sortid']] = row
				result		= 0,rs
			else:
				result = res, desc
		elif action == 'getcurrentsubtag':	
			"""获取当前标签的下一级分类(这个是省份城市区类)
			Args:
				sortid int 为0是返回一级分类
			"""	
			sortid			= int(params.get('sortid',0))
			if not sortid:
				kw['where']	= "sortid>101000 AND sortid<102000"
			else:
				kw['where']	= 'sortid>%s and sortid <%s'% ((sortid*1000),  ((sortid+1)*1000))
			kw['fields']	= params.get('fields','id,name,sortid,order_sort')
			kw['order']		= "order_sort DESC, sortid ASC"
			res, desc		= dbhandle.query(kw)
			if res ==0:
				rs			= {}
				for row in desc:
					rs[row['sortid']] = row
				result		= 0,rs
			else:
				result = res, desc

		elif action == 'getbytagid':	
			"""根据sortid获取对应的标签信息
			"""	
			sortid			= params.get('sortid',0)
			if not sortid :
				raise falcon.HTTPBadRequest('illegal_argument','sortid must provided')
			if type(sortid) in (tuple,list):
				sortid = ','.join(sortid)

			kw['where']	= 'sortid in (%s)'% sortid
			res, desc		= dbhandle.query(kw)
			if res ==0:
				rs			= {}
				for row in desc:
					rs[row['sortid']] = row
				result		= 0,rs
			else:
				result = res, desc
				
		elif action == 'getalltags':	
			"""获取所有标签值
			"""	
			kw['where'] = "sortid=101OR (sortid>101000 AND sortid<102000) OR (sortid>101000000 AND sortid<102000000) OR (sortid>101000000000 AND sortid<102000000000)"
			result			= dbhandle.query(kw)

		elif action == 'gettags':	
			"""获取标签信息(所有或者一级或者id名称对应信息)
	   			Args:
	   				sortid		标签id
	  									0 显示所有标签
										1 显示一级标签,
	  									2 就显示二级标签,
									其它情况如:
	 									sortid="101,102"显示sortid=>名称对应的标签数组
			"""	
			sortid			= params.get('sortid','1')
			kw['fields']	= params.get('fields','id,name,sortid')
			if sortid in ['0','1','2']:
				sortid = int(sortid)
				if sortid == 1:
					kw['where'] = "sortid>1000 and sortid <1000000 "
				elif sortid ==2:
					kw['where'] = "sortid>1000000 and sortid <1000000000"
			else:
				if type(sortid) in (tuple,list):
					sortid = ','.join(sortid)	
				kw['where'] = "sortid in (%s) " % sortid
							
			res, desc		= dbhandle.query(kw)
			if res ==0:
				rs			= {}
				for row in desc:
					rs[row['sortid']] = row
				result		= 0,rs
			else:
				result = res, desc

		elif action == 'getexpotags':	
			"""获取展会省份标签信息(所有或者一级或者id名称对应信息
	   			Args:
	   				tag_id		标签id
	  									0 显示所有标签
										1 显示一级标签,
	  									2 就显示二级标签,
									其它情况如:
	 									tag_id="101,102"显示tag_id=>名称对应的标签数组
			"""	
			kw['dbname']	= 'expo'
			kw['table']		= 'expo_area'
			tag_id			= params.get('tag_id','1')	
		
			kw['fields']	= params.get('fields','id,name,tag_id')
			if type(kw['fields']) in (tuple,list):
				if 'tag_id' not in kw['fields']:
					kw['fields'].append('tag_id')
				kw['fields'] = ','.join(kw['fields'])
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

		elif action == 'getexopsubtag':	
			"""获取展会省市一级标签的所有子类
			"""	
			kw['dbname']	= 'expo'
			kw['table']		= 'expo_area'
			kw['fields']	= params.get('fields','id,name,tag_id,order_sort')
			if type(kw['fields']) in (tuple,list):
				if 'tag_id' not in kw['fields']:
					kw['fields'].append('tag_id')
				kw['fields'] = ','.join(kw['fields'])
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
			
		else:
			raise falcon.HTTPError(falcon.HTTP_404,'invalid_grant','invalid action %s' % action)	
			
		if result[0] == -1:
			raise falcon.HTTPBadRequest('invalid_sql_syntax',str(result[1]))

		result={'result':result[1]}
		resp.body = JSONEncoder().encode(result)	
		
		
#--------
#注册模块路由
#--------

app.add_route('/%s/query/common/{action}'% __Version,common())
