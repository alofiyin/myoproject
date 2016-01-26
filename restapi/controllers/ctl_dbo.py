#_*_coding:utf-8_*_
import falcon
import gzip,json,time
from pprint import pprint
import sconf
from hashlib import md5
from utils import JSONEncoder
import logging
from myapp import app
import dbrest as	dbhandle
__Version = '1.0'
logger = logging.getLogger('main')
	
class rest_mysql:
	"""mysql 数据库写入操作
	"""
	def __init__(self):
		self.databases	= sconf.get_db_list(False)
		
	def on_get(self,req,resp,dbname,table):
		if '.' in table:
			raise falcon.HTTPBadRequest('invalid_grant',"invalid table name %s" % table)
		kw 			= req.params
		kw['table']	= table
		kw['dbname']= dbname

		if dbname in self.databases:
			result = dbhandle.getlist(kw)
			if result[0] == -1:
				raise falcon.HTTPBadRequest('invalid_sql_syntax',result[1]
			)
		else:
			raise falcon.HTTPBadRequest('invalid_grant',"invalid databases name %s" % dbname)
		logger.info("t:%s bodylen:%s" %(req.date,len(str(result))))
		result={'result':result[1]}
		resp.body = JSONEncoder().encode(result)

					
	def on_post(self,req,resp,dbname,table):
		if '.' in table:
			raise falcon.HTTPBadRequest('invalid_grant',"invalid table name %s" % table)
		kw = req.context
		kw['dbname']	= dbname
		kw['table']		= table
		if dbname in self.databases:
			result = dbhandle.insert(kw)
			if result[0] == -1:
				raise falcon.HTTPBadRequest('invalid_sql_syntax',result[1])
		else:
			raise falcon.HTTPBadRequest('invalid_grant',"invalid databases name %s" % dbname)
		logger.info("t:%s bodylen:%s" %(req.date,len(str(result))))
		result={'result':result[1]}
		resp.body = JSONEncoder().encode(result)

	def on_put(self,req,resp,dbname,table):
		if '.' in table:
			raise falcon.HTTPBadRequest('invalid_grant',"invalid table name %s" % table)
		kw = req.context
		kw['dbname']	= dbname
		kw['table']		= table
		if dbname in self.databases:
			result = dbhandle.update(kw)
			if result[0] == -1:
				raise falcon.HTTPBadRequest('invalid_sql_syntax',result[1])
		else:
			raise falcon.HTTPBadRequest('invalid_grant',"invalid databases name %s" % dbname)
		logger.info("t:%s bodylen:%s" %(req.date,len(str(result))))
		result={'result':result[1]}
		resp.body = JSONEncoder().encode(result)
		
	def on_delete(self,req,resp,dbname,table):
		if '.' in table:
			raise falcon.HTTPBadRequest('invalid_grant',"invalid table name %s" % table)
		kw = req.context
		kw['dbname']	= dbname
		kw['table']		= table
		kw['id']		= req.get_param('id','')
		if dbname in self.databases:
			result = dbhandle.delete(kw)
			if result[0] == -1:
				raise falcon.HTTPBadRequest('invalid_sql_syntax',str(result[1]))
		else:
			raise falcon.HTTPBadRequest('invalid_grant',"invalid databases name %s" % dbname)
		logger.info("t:%s bodylen:%s" %(req.date,len(str(result))))
		result={'result':result[1]}
		resp.body = JSONEncoder().encode(result)
		#resp.body = json.dumps(req.context)
		
class rest_mysql_query:
	"""基本数据查询服务
	"""
	def __init__(self):
		self.databases	= sconf.get_db_list()
		
	def on_get(self,req,resp,dbname,table,action):
		if dbname not in self.databases:
			raise falcon.HTTPError(falcon.HTTP_404,'invalid_grant',"invalid databases name %s" % dbname)
		if '.' in table:
			raise falcon.HTTPError(falcon.HTTP_404,'invalid_grant',"invalid table name %s" % table)			
		kw 			= req.params
		kw['table']	= table
		kw['dbname']= dbname
		if action == 'getbyid':
			if 'ids' not in kw:
				raise falcon.HTTPBadRequest('illegal_argument','ids must provided')
			result = dbhandle.getbyid(kw)
		
		elif action == 'getcount':
			result = dbhandle.getcount(kw)
			
		elif action == 'getlist':
			result = dbhandle.getlist(kw)
		
		else:
			raise falcon.HTTPError(falcon.HTTP_404,'invalid_grant','invalid action %s' % action)
			
		if result[0] == -1:
			raise falcon.HTTPBadRequest('invalid_sql_syntax',str(result[1]))

		result={'result':result[1]}
		resp.body = JSONEncoder().encode(result)

#--------
#注册模块路由
#--------
app.add_route('/%s/dbo/{dbname}/{table}'% __Version,rest_mysql())
app.add_route('/%s/dbo/{dbname}/{table}/{action}'% __Version,rest_mysql_query())