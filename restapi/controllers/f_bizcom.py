#_*_coding:utf-8_*_
import falcon
from cls_base import cache_get,cache_set,get_cnf_val
import gzip,json,time
from pprint import pprint
import biz_com
import sconf
from hashlib import md5
from utils import JSONEncoder
import logging
from myapp import app
#
#数据接口-标签
#
#------------------------
#取得标签列表-从缓存取
#------------------------

logger = logging.getLogger('main')
class f_bizcom:
	def __init__(self):
		pass
	def on_post(self,req,resp,action):
		result = [-108,"action %s not found."% action ]
		kw = req.context['doc']
		biznum = kw.get('biznum','')
		bizcnf = get_cnf_val(biznum,sconf.BIZ)
		if not bizcnf:
			sconf.err_handle.biznum_not_config
			raise falcon.HTTPError(falcon.HTTP_701,
                                   sconf.err_handle.biznum_not_config[1],
									)
		kw['bizcnf'] = bizcnf
		#执行action
		if action == 'gettags':
			#传入参数
			prama = kw.get("prama",{})
			biznum = kw.get('biznum')
			#业务配置
			bizcnf = kw.get("bizcnf")
			tag_id = str(prama.get('tag_id',bizcnf['prama']['tag_id']))
		
			lv2rows = prama.get('lv2rows',bizcnf['prama']['lv2rows'])
			lv3rows = prama.get('lv3rows',bizcnf['prama']['lv3rows'])
			ttl     = prama.get('ttl',bizcnf['prama']['ttl'])
			ckey = "%s.%s%s%s" %(biznum,tag_id,lv2rows,lv3rows)
			result = cache_get(ckey)
			if result:
				result = 0,json.loads(res)
			
			else:
				result = biz_com.gettags(kw)
				if result[0] == 0 and result[1]:
					cache_set(ckey,json.dumps(result[1]),ttl)	

		resp.body = JSONEncoder().encode(result)
	def on_get(self,req,resp,action):
		result = [-108,"action %s not found."% action ]
		#kw = req.context['doc']
		kw = {"biznum":"com.corp_targ","prama":{"tag_id":101,"lv2rows":13,"lv3rows":1}}
		biznum = kw.get('biznum','')
		bizcnf = get_cnf_val(biznum,sconf.BIZ)
		if not bizcnf:
			sconf.err_handle.biznum_not_config
			raise falcon.HTTPError(falcon.HTTP_701,
                                   sconf.err_handle.biznum_not_config[1],
									)
		kw['bizcnf'] = bizcnf
		if action == 'gettags':
			result = gettagsAction(kw)
			logger.info("t:%s bodylen:%s" %(req.date,len(str(result))))
		resp.body = JSONEncoder().encode(result)
def gettagsAction(kw):
	"""标签缓存key: biz:prod:targ
	参数说明:
		bizcnf:业务配置信息
		tag_id:父标签
		lv2rows:二级标签提取数量
		lv3rows:三级标签提取数量
	"""
	#传入参数
	prama = kw.get("prama",{})
	biznum = kw.get('biznum')
	#业务配置
	bizcnf = kw.get("bizcnf")
	tag_id = str(prama.get('tag_id',bizcnf['prama']['tag_id']))

	lv2rows = prama.get('lv2rows',bizcnf['prama']['lv2rows'])
	lv3rows = prama.get('lv3rows',bizcnf['prama']['lv3rows'])
	ttl     = prama.get('ttl',bizcnf['prama']['ttl'])
	ckey = "%s.%s%s%s" %(biznum,tag_id,lv2rows,lv3rows)
	res = cache_get(ckey)
	if res:
		return 0,json.loads(res)
	res = biz_com.gettags(kw)
	if res[0] == 0 and res[1]:
		cache_set(ckey,json.dumps(res[1]),ttl)	
	return res
	

#------------------------
#根据标签取公司数据
#------------------------		
	
def listAction(kw):
	#传入参数
	prama	= kw.get("prama",{})
	bizcnf	= kw.get('bizcnf')
	ttl		= prama.get('ttl',bizcnf['prama']['ttl'])
	md		= md5(json.dumps(prama).encode()).hexdigest()
	ckey	= "%s.%s" % (kw['biznum'],md)
	res = cache_get(ckey)
	if res:
		return 0,json.loads(res)

	res = biz_com.list(kw)
	if res[0] == 0 and res[1]:
		cache_set(ckey,json.dumps(res[1]),ttl)	
	return res

app.add_route('/bizcom/{action}',f_bizcom())