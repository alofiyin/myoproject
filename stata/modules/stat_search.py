#_*_coding:utf-8_*_
#统计模板
from stat_base import get_host_by_data,get_cnf_val
import sconf
import mysqlwrap
from sphinxwrap import sphinx
import rediswrap
import utils,time
from pprint import pprint

				
def sphinx2redis(cnfkey):
	"""通过配置文件，获取统计数据
	"""
	#取业务配置
	bizcnf = get_cnf_val(cnfkey,sconf.BIZ)	
	if not bizcnf:
		return sconf.err_handle.biznum_not_config
	rdb = rediswrap.get_redis('cache')

	for i in range(0,len(bizcnf['prama'])):
		itm = bizcnf['prama'][i]
		source = itm['source'].split('.')
		if source[1] == 'sphinx':
			host_info = get_host_by_data(itm['source'])
			if  not host_info :
				return sconf.sphinx_index_not_found
			
			sp = sphinx(host_info['host'],host_info['port'])
			expression = itm['expression']
			expression['index'] = source[2]
			total_found = 0
			while True:
				#if total_found >0:
				#	if expression['pageSize'] * expression['page'] >=total_found:
				#		break
				#	expression['page'] +=1
					
				sp.initQuery(itm['expression'])
				rs = sp.RunQueries()
				pprint(rs)
				if rs and rs[0]['status']==0:
					total_found = rs[0]['total_found']
					_items = {}
					for row in rs[0]['matches']:
						if itm['key'] in row['attrs'] and itm['value'] in row['attrs']:
							_items[row['attrs'][itm['key']]]=row['attrs'][itm['value']]
					if _items:
						print(_items)
						#res = rdb.mset(cnfkey,_items)
						
				else:
					print(sp._error)
					break
				break

def sphinx2redis_ex(cnfkey):
	"""通过配置文件，获取统计数据
	"""
	#取业务配置
	bizcnf = get_cnf_val(cnfkey,sconf.BIZ)	
	if not bizcnf:
		return sconf.err_handle.biznum_not_config
	rdb = rediswrap.get_redis('cache')
	dbinfo = get_host_by_data("base.mysql.biz72_product")
	dbinfo['dbname']="biz72_product"
	db  = mysqlwrap.dbclass(dbinfo)
	db.connect()
	sql = "select tag_id from pro_tag where tag_id>100 and tag_id<200"
	res,desc = db.query(sql)
	print("rows:",len(desc))
	source="base.sphinx.IDX_com_corp_dist"
	host_info = get_host_by_data(source)
	sp = sphinx(host_info['host'],host_info['port'])
	prama = {
					"querymod":"SPH_MATCH_EXTENDED2",
					"pageSize":1,
					"page":1,
					"intType":{
            		},
            		"index":"IDX_com_corp_dist"
			}
	itm1 = {}
	itm2 = {}
	itm3 = {}
	x=0
	st = int(time.time())
	for row in desc:
		x+=1
		if x%100==0:
			print(x,time.time()-st)
		tag_len = len(str(row['tag_id']))
		if tag_len == 3:
			f = "r_com"
		elif tag_len == 6:
			f = "c_com"
		elif tag_len == 9:
			f = "com"
		prama['intType'][f]=str(row['tag_id'])
		#prama['intType']["com"]='101105105'
		sp.initQuery(prama)
		rs = sp.RunQueries()

		if rs and rs[0]['status']==0:
			total_found = rs[0]['total_found']
			print("tag_id",row['tag_id'],"total_found",total_found)
			if total_found >0:
				rdb.hset('stat2cach.tags_corp',row['tag_id'],total_found)
			if tag_len == 3:
				itm1[row['tag_id']]=total_found
			elif tag_len == 6:
				itm2[row['tag_id']]=total_found
			elif tag_len == 9:
				itm3[row['tag_id']]=total_found
		else:
			print(sp._error)

	print("time:",time.time()-st)
	print("itm1","len:",len(itm1),"sum:",sum(list(itm1.values())))		
	print("itm2","len:",len(itm2),"sum:",sum(list(itm2.values())))	
	print("itm3","len:",len(itm3),"sum:",sum(list(itm3.values())))	
if __name__=="__main__":
	import json
	sconf.SYS = json.loads("".join(open('../conf/sys.json').read().split()))
	sconf.HOST = json.loads("".join(open('../conf/host.json').read().split()))
	sconf.BIZ['stat2cach'] = json.loads(open("../conf/biz_stat2cach.json").read().replace('\n','').replace('\t',''))
	sconf.DATA_SOURC = json.loads("".join(open('../conf/databases.json').read().split()))
	#biz_info = json.loads("".join(open('../conf/biz.json').read().split()))
	
	#加载数据库
	mysqlwrap.setup_db('default',sconf.SYS['mysql'])
	mysqlwrap.pool_monitor()
	rediswrap.setup_redis('cache',sconf.SYS['redis']['host'],sconf.SYS['redis']['port'])
	key = "stat2cach.tags_corp_top"
	#key = "stat2cach.tags_prod"
	#print (  init_group('pst_corp',biz_info['pst_corp']) )
	res = sphinx2redis(key)
	print(res)			