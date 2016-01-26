#_*_coding:utf-8_*_
#api接口测试
import falcon
from httpwrap import HttpWrap
from utils import JSONEncoder
import myapp
import json

class clt_test:
	def __init__(self):
		self.http 	= HttpWrap()
		self.host	= "http://test.api.biz72.com/index.php?r="
		
	def on_get(self,req,resp,action):
		mod,act = action.split('.')
		if action == "proinfo.search":
			param = {}
			opt = [];
			row = {}
			row["page"]		= 1
			row["pageSize"]	= 20
			row["keyw"]		= "机械"		
			opt.append(row)
			param["param"] 		= opt
			param["field1"]		= "id,title"
			param["field2"]		= "id,desc"
			url = "%s/%s/%s" % (self.host,mod,act)
			res = self.http.request(url,'POST',param)
			res = self.http.read(res)
			res = JSONEncoder().encode(res)
			resp.body = json.dumps(res, indent=1)


myapp.app.add_route('/test/{action}',clt_test())