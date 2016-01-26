#_*_coding:utf-8_*_
from cls_base import get_host_by_data,get_cnf_val
import rediswrap
import sconf
from mysqlwrap import dbclass
import biz_tag as tagsclass
from sphinxwrap import sphinx
import gzip,json,time
from pprint import pprint
from utils import JSONEncoder
#
#数据接口-标签
#
#------------------------
#取得标签列表-从缓存取
#------------------------
def gettags(kw):
	"""标签缓存key: biz:prod:targ
	test: 	
     curl -l -H "Content-Type: application/json" -X POST -d  '{"biznum":"tags.corp","tag_id":101,"lv2rows":13,"lv3rows":1}'     http://192.168.10.126:6000/biz_tags/gettags
	参数说明:
		biznum:业务配置标识
		tag_id:父标签
		lv2rows:二级标签提取数量
		lv3rows:三级标签提取数量
	"""
	biznum = kw.get('biznum','')
	biznum = 'com.corp_targ'
	sort = ""
	tag_id = str(kw.get('tag_id',""))
	tag_id_len = 0 if len(tag_id) < 3 else len(tag_id)
	lv2rows = kw.get('lv2rows',6)
	lv3rows = kw.get('lv3rows',12)
		
	if not biznum:
		return [-6,'parameter biznum not set.']
	bizcnf = get_cnf_val(biznum,sconf.BIZ)
	#取业务配置
	if not bizcnf:
		return sconf.err_handle.biznum_not_config

	ttl     = bizcnf.get('ttl',600)
	isort   = bizcnf.get('sort','total_num')
	#取数据
	rdb = rediswrap.get_redis('cache')
	print(dir(rdb))
	ckey = "%s.%s%s%s%s" %(biznum,sort,tag_id,lv2rows,lv3rows)
	res = rdb.get(ckey)
	
	if res:
		#return 0,JSONEncoder().encode(res)
		return 0,{}
		
	res = rdb.get("biz:targ.%s"%bizcnf['table'])
	
	if not res:
		s,res = tagsclass.prod_targs(biznum)
	else:
		res = json.loads(res)
	#组织数据
	#tag_id of level 1
	data={}
	if tag_id_len ==3 and tag_id in res and 'extn' in res[tag_id]:
		data = res[tag_id]
	elif tag_id_len ==6:
		data = res[str(tag_id)[:3]]['extn'][tag_id]
	#tag_id of all
	elif not tag_id:
		data={'info':{'tag_id':0}}
		data['extn'] = res
	if data and 'extn' in data:
		res = tag_recursion(data,lv2rows,lv3rows)
		rdb.setex(ckey,json.dumps(res),ttl)
		#return 0,res 
		return 0,{}
	else:
		return 0,{}
	
def tag_recursion(data,n1=0,n2=0):
	"""递归组织标签
	参数说明:
	data 数据源 
		{"info":{"tag_id":"","total_num":"".....},
		"extn":{"info":{"tag_id":"","total_num":"".....},
				"extn":{"info":{"tag_id":"","total_num":"".....},
				}
			}
		}
	n1:二级标签提取数量
	n2:三级标签提取数量
	返回格式：
	{'info':{"tag_id":"","total_num":"".....},
	 'extn':[{'info':{"tag_id":"","total_num":"".....},
	 		'extn'{}...
	 		]
	 }
	"""
	
	res={'info':data['info']}
	if 'extn' not in data or not data['extn']:
		return res
	res['extn']=[]
	#排序
	sortList=[]
	for k,v in data['extn'].items():
		try:
			sortList.append([sum(json.loads(v['info']['total_num']).values()),k])
		except:
			if v['info']['total_num'] not in(0,'0'):
				sortList.append(row['info']['total_num'],k)				
	#sortList = [[sum(json.loads(k2['info']['total_num']).values()),k2['info']['tag_id']] for k2 in data['extn']]
	sortList.sort(reverse=True)
	tag_id = int(data['info']['tag_id'])
	n = n1 if tag_id >=100 and tag_id <1000 else n2
	if tag_id == 0:
		n = 0
	i=0
	for v,tid in sortList:
		if n and i==n:
			break
		i+=1
		if 'extn' in data['extn'][tid] and data['extn'][tid]['extn']:
			res['extn'].append(tag_recursion(data['extn'][tid],n1,n2))
		else:
			res['extn'].append(data['extn'][tid])
	return res
	
#------------------------
#取得标签列表-直接从数据库取
#------------------------
def gettags_base(kw):
	"""标签缓存key: biz:prod:targ
	"""
	biznum = kw.get('biznum','')
	sort = kw.get('sort','pro')
	tag_id = int(kw.get('tag_id',0))
	tag_id_len = 0 if len(str(tag_id)) < 3 else len(str(tag_id))
	if not biznum:
		return [-6,'parameter biznum not set.']
	bizcnf = get_cnf_val(biznum,sconf.BIZ)
	#取业务配置
	if not bizcnf:
		return sconf.err_handle.biznum_not_config
	lv2rows = kw.get('lv2rows',bizcnf['lv2rows'])
	lv3rows = kw.get('lv3rows',bizcnf['lv3rows'])
	ttl     = kw.get(bizcnf['ttl'],600)
	isort   = kw.get(bizcnf['sort'],'total_num')
	#取数据库配置
	dbinfo = get_host_by_data(bizcnf['source'])
	if not dbinfo:
		return sconf.err_handle.db_not_config
	dbinfo['dbname']=bizcnf['source'].split('.')[-1]
	rdb = rediswrap.get_redis('cache')
	
	res = rdb.get("%s.%s%s%s%s" %(biznum,sort,tag_id,lv2rows,lv3rows))
	if res:
		return gzip.decompress(res)
	db = dbclass(dbinfo)
	res,desc = db.connect()
	
	if res == -1:
		return sconf.err_handle.db_err
	sql_item={}
	sql_item['table'] = bizcnf['table']
	sql_item['fields'] = bizcnf['fields']
	if tag_id_len ==3:
		sql_item['where'] = "tag_id = %s or (tag_id>%s000 and tag_id <%s000) or (tag_id>%s000000 and tag_id<%s000000) " % (tag_id,tag_id,(tag_id+1),tag_id,(tag_id+1))
	elif tag_id_len >=6:
		sql_item['where'] = "tag_id = %s or (tag_id>%s000 and tag_id <%s000)" % (tag_id,tag_id,(tag_id+1))

	sql_item['order'] = "tag_id asc"
	pprint.pprint(kw)
	pprint.pprint(sql_item)
	res,desc = db.query(sql_item)

	if res == -1:
		return sconf.err_handle.db_err
	if desc:
		tag_id_len = 3 if tag_id_len==0 else tag_id_len
		obj = {}
		for row in desc:
			tid = str(row['tag_id'])
			if len(tid)-tag_id_len ==0:
				obj[row['tag_id']]={"info":row}
			elif len(tid) - tag_id_len ==3:
				pid = int(tid[:tag_id_len])
				if 'extn' not in  obj[pid]:
					obj[pid].update({'extn':{"info":row}})
				obj[pid]['extn'].update({row['tag_id']:row})
			elif len(tid) - tag_id_len==6:

				ppid = int(tid[:tag_id_len])
				pid =  int(tid[:tag_id_len+3])
				if 'extn' not in  obj[ppid]['extn'][pid]:
					obj[ppid]['extn'][pid].update({'extn':{"info":row}})
				obj[ppid]['extn'][pid].update({row['tag_id']:row})
		#pprint.pprint(obj)
		return 0,obj
								
#------------------------
#根据标签取公司数据
#------------------------		
	
def corplist(kw):
	"""
	test: 	
     curl -l -H "Content-Type: application/json" -X POST -d  '{"biznum":"tags.corplist","tag_id":[101]}'     http://192.168.10.126:6000/biz_tags/corplist
	"""	
	tag_id = kw.get('tag_id',[])
	biznum = kw.get('biznum','')

	if not biznum:
		return [-6,'parameter biznum not set.']
	bizcnf = get_cnf_val(biznum,sconf.BIZ)
			
	#取业务配置
	if not bizcnf:
		return sconf.err_handle.biznum_not_config
		
	pageSize = kw.get('pageSize',bizcnf['search']['expression']['pageSize'])
	page = kw.get('page',bizcnf['search']['expression']['page'])
	#连接搜索引擎
	host_info = get_host_by_data(bizcnf['search']['source'])
	if  not host_info :
		return sconf.sphinx_index_not_found
	sp = sphinx(host_info['host'],host_info['port'])
	
	expression = bizcnf['search']['expression']
	expression['index'] = bizcnf['search']['source'].split('.')[-1]
	expression['pageSize']=pageSize
	expression['page']=page
	st = int(time.time())
	for tid in tag_id:
		tag_len = len(str(tid))
		if tag_len == 3:
			f = "r_com"
		elif tag_len == 6:
			f = "c_com"
		elif tag_len == 9:
			f = "com"
		#exp = expression.copy()
		expression['intType'][f]=str(tid)
		sp.initQuery(expression)
	rs = sp.RunQueries()
	print("search_time:",time.time()-st)
	result = []
	st = int(time.time())
	if rs:
		#连接数据库
		dbinfo = get_host_by_data(bizcnf['data']['source'])
		dbinfo['dbname'] = bizcnf['data']['source'].split('.')[-1]
		db = dbclass(dbinfo)
		db.connect()
		for row in rs:
			sql_item =  bizcnf['data'].copy()
			ids = [str(k['id']) for k in row['matches']]
			print("ids:",ids)
			sql_item['where'] = sql_item['where'] % ",".join(ids)
			res,desc = db.query(sql_item)
			if res ==0 and desc:
				result.append(desc)
	else:
		result.append([])
	#print("search_time:",time.time()-st)
	#pprint(result)	
	#print(sp._error)
	return [0,result]
#------------------------
#根据标签取产品数据
#------------------------		
	
def prodlist(kw):
	"""
	test: 	
     curl -l -H "Content-Type: application/json" -X POST -d  '{"biznum":"tags.corplist","tag_id":[101]}'     http://192.168.10.126:6000/biz_tags/prodlist
	"""	
	tag_id = kw.get('tag_id',[])
	biznum = kw.get('biznum','')

	if not biznum:
		return [-6,'parameter biznum not set.']
	bizcnf = get_cnf_val(biznum,sconf.BIZ)
			
	#取业务配置
	if not bizcnf:
		return sconf.err_handle.biznum_not_config
		
	pageSize = kw.get('pageSize',bizcnf['search']['expression']['pageSize'])
	page = kw.get('page',bizcnf['search']['expression']['page'])
	#连接搜索引擎
	host_info = get_host_by_data(bizcnf['search']['source'])
	if  not host_info :
		return sconf.sphinx_index_not_found
	sp = sphinx(host_info['host'],host_info['port'])
	
	expression = bizcnf['search']['expression']
	expression['index'] = bizcnf['search']['source'].split('.')[-1]
	expression['pageSize']=pageSize
	expression['page']=page
	st = int(time.time())
	for tid in tag_id:
		tag_len = len(str(tid))
		if tag_len == 3:
			f = "r_tag_id"
		elif tag_len == 6:
			f = "c_tag_id"
		elif tag_len == 9:
			f = "_tag_id"
		#exp = expression.copy()
		expression['intType'][f]=str(tid)
		sp.initQuery(expression)
	rs = sp.RunQueries()
	print("search_time:",time.time()-st)
	result = []
	st = int(time.time())
	if rs:
		#连接数据库
		dbinfo = get_host_by_data(bizcnf['data']['source'])
		dbinfo['dbname'] = bizcnf['data']['source'].split('.')[-1]
		db = dbclass(dbinfo)
		db.connect()
		for row in rs:
			sql_item =  bizcnf['data'].copy()
			ids = [str(k['id']) for k in row['matches']]
			print("ids:",ids)
			sql_item['where'] = sql_item['where'] % ",".join(ids)
			res,desc = db.query(sql_item)
			if res ==0 and desc:
				result.append(desc)
	else:
		result.append([])
	#print("search_time:",time.time()-st)
	#pprint(result)	
	#print(sp._error)
	return [0,result]