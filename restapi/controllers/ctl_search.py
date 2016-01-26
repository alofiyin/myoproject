#_*_coding:utf-8_*_
import falcon
import gzip,json,time
from pprint import pprint
import sconf
from hashlib import md5
from utils import JSONEncoder
import logging
from myapp import app
import sp_search as	sphandle

__Version = '1.0'
	
		
class search:
	"""sphinx搜索服务
	"""
	def __init__(self):
		self.indexs	= sconf.get_search_list()
		
	def on_get(self,req,resp,index):
		if index not in self.indexs:
			raise falcon.HTTPError(falcon.HTTP_404,'invalid_grant',"invalid index name %s" % index)
			
		params			= req.params
		opt				= params.get('opt')
		kw				= sphandle.parse(opt)
		kw['keyw']		= params.get('keyw')
		kw['page']		= int(params.get('page',1))
		kw['pageSize']	= int(params.get('pagesize',sconf.PAGE_SIZE))
		kw['index']		= index
		kw['orderBy']	= params.get('order')
		kw['groupBy']	= params.get('group')
		kw['fields']	= params.get('fields','')
		result			= sphandle.search(kw)	

		if result[0] == -1:
			raise falcon.HTTPError(falcon.HTTP_400,'searchd error',str(result[1]))

		result={'result':result[1]}
		resp.body = JSONEncoder().encode(result)

	def on_post(self,req,resp,index):
		if index not in self.indexs:
			raise falcon.HTTPError(falcon.HTTP_404,'invalid_grant',"invalid index name %s" % index)
			
		params			= req.context
		params['index']		= index
		result			= sphandle.search(kw)	
		if result[0] == -1:
			raise falcon.HTTPError('invalid_sql_syntax',str(result[1]))

		result={'result':result[1]}
		resp.body = JSONEncoder().encode(result)
#--------
#注册模块路由
#--------
app.add_route('/%s/search/{index}'% __Version,search())
