#_*_coding:utf-8_*_
#统计模板
import stat_base
import sconf
import mysqlwrap
from httpwrap import HttpWrap
from sphinxwrap import sphinx
import rediswrap
import utils,json

#-------参数配置文件-----#				
def get_cnf_val(k,dist):
	"""递归取出joson配置信息值
	"""
	if '.' not in k :
		return dist[k] if k in dist else None
	kesy = k.split('.')		
	if kesy[0] in dist:
		kk = k[k.index('.')+1:]
		tmp = dist[kesy[0]]
		return get_cnf_val(kk,tmp)
	else:
		return None
def get_host_by_data(k):
	"""取出数据服务器信息
	"""
	host_key = get_cnf_val(k,sconf.DATA_SOURC)
	if host_key:
		return 	get_cnf_val(host_key,sconf.HOST)
	return None	
#-----数据操作 ----#
def reg_items_mysql(name,info):
	"""items来源于mysql数据表，自动注册items
	"""
	k = info['source']
	dbinfo = get_host_by_data(k)
	if not dbinfo:
		return [-1,"%s not find." % k]
	dbinfo['dbname'] = k.split('.')[-1]
	db = mysqlwrap.dbclass(dbinfo)
	res,desc = db.connect()
	if res ==-1:
		return res,desc
	
	idfield = info.get("id","id")
	key_prefix = info.get("key_prefix","")
	sql_item={}
	sql_item['table']=info['table']
	sql_item['fields']="%s,%s,%s" %(idfield,info['key'],info['name'])
	where =  info['where'] if 'where' in info and info['where'] else ""
	sql_item['where'] = where
	sql_item['limit'] = 1000
	id = 0
	item_total=0	
	while True:		
		sql_item['where'] = "%s and %s>%s" %(where,idfield,id) if where else "%s>%s" %(idfield,id)
		res,desc = db.query(sql_item)
		if res==-1 or res==0 and not desc:
			 break
		itm=[]
		for row in desc:
			itm.append([row[info['name']],row[info['key']]])
			print(itm[-1])
			id = row[idfield]
		rs,ds = stat_base.reg_items(name,itm,key_prefix)
		#print(rs,ds)
		if rs==0:
			item_total+=len(itm)
	stat_base.reg_items2redis(name)
	return [0,item_total]
	
def init_group(name,info):
	"""
	通过配置文件初始化统计组(group)和统计项(items)
	"""
	res,desc = stat_base.reg_group(name,info)
	if res==0 and desc:
		for row in info['item_from']:
			rs ,ds = reg_items_mysql(name,row)
	return res, desc

def get_stat_data(name,info):
	"""通过配置文件，获取统计数据
	"""
	#url提交模式
	http = HttpWrap()
	http.set_header('Content-type','application/json')
	url = "http://192.168.10.126:1985/api/set"
	
	for i in range(0,len(info['history_from'])):
		itm = info['history_from'][i]
		source = itm['source'].split('.')
		if source[1] == 'sphinx':
			host_info = get_host_by_data(itm['source'])
			if  not host_info :
				return [-1,"key erro %s not in sysconfig." % row['source']]
			
			sp = sphinx(host_info['host'],host_info['port'])
			expression = itm['expression']
			expression['index'] = source[2]
			total_found = 0
			while True:
				if total_found >0:
					if expression['pageSize'] * expression['page'] >=total_found:
						break
					expression['page'] +=1
					
				sp.initQuery(itm['expression'])
				rs = sp.RunQueries()
				if rs and rs[0]['status']==0:
					total_found = rs[0]['total_found']
					_items = {}
					for row in rs[0]['matches']:
						_items["%s%s" % (itm['key_prefix'],row['attrs'][itm['key']])]=[row['attrs'][itm['value']],utils.timestamp(0,'d')]
					if _items:
						data = json.dumps({'gkey':name,'data':_items})
						_rs = http.request(url,"POST",data)
						rs = http.read(_rs)
						print(rs)
				else:
					print(sp._error)
					break
				
if __name__=="__main__":
	import json
	sconf.SYS = json.loads("".join(open('../conf/sys.json').read().split()))
	sconf.HOST = json.loads("".join(open('../conf/host.json').read().split()))

	sconf.DATA_SOURC = json.loads("".join(open('../conf/databases.json').read().split()))
	#biz_info = json.loads("".join(open('../conf/biz.json').read().split()))
	biz_info = json.loads(open('../conf/biz.json').read().replace('\n','').replace('\t',''))
	#加载数据库
	mysqlwrap.setup_db('default',sconf.SYS['mysql'])
	mysqlwrap.pool_monitor()
	rediswrap.setup_redis('default',sconf.SYS['redis']['host'],sconf.SYS['redis']['port'])
	#print (  init_group('pst_corp',biz_info['pst_corp']) )
	print(get_stat_data('pst_corp',biz_info['pst_corp']))				