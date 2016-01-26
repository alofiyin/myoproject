#_*_coding:utf-8_*_
#统计系统基本操作函数集
from  sphinxwrap import sphinx
import json,time
import sconf
import mysqlwrap as mysqldb
import rediswrap 
import utils
#----------group操作----------#
#存放item key id的redis field前缀
RD_ITM_KEY_PRFX = "stat:items:"
#存放临时统计数据的redis field前缀
RD_ITM_HST_TMP_PRFX = "stat:hst:tmp:"

class err_handle:
	loss_arg = [-6,'缺失参数']
	gkey_not_set = [-1,'未检测到参数gkey.']
	items_not_set = [-2,'未检测到参数items']
	db_err = [-100,'数据库操作错误']
	gkey_not_found = [-3,'gkey未注册']
	data_not_found = [-4,'未检测到参数data']
	item_exis = [-5,'item已存在']
	sphinx_param_not_set = [-10,"没有设置参数组param"]
	sphinx_index_not_found = [-11,'索引不存在']
	
def reg_group(gkey,info):
	"""
	注册group
	参数说明:
	 gkey group的标识
	 info 组信息 
	返回值:[status,info]
	status: 0 成功
	        -100 数据库错误
	"""
	if gkey == 'default':
		return [0, 1]
	pid = info.get('pid',1)
	name = info.get('name')
	items_mrk = info.get('items_mrk','')
	history_mrk = info.get('history_mrk',items_mrk)
	#检查group是否存在，如不存则插入
	stat_db = mysqldb.get_db()
	res,desc = get_groups([gkey])
	#print(res,desc)
	if res==0 and not desc:
		data = {'name':name,'pid':1,'gkey':gkey,'items_mrk':items_mrk,'history_mrk':history_mrk}
		rs, des = stat_db.insert('stat_item_group',data)
		gid = des
	else:
		gid = desc[0]['gid']
	
	#检查项目表与记录表是否存在，不存在创建
	itesm_tabse_ddl = """
	  Create Table  stat_item_%s (
	  id int(11) NOT NULL AUTO_INCREMENT COMMENT '项目id号',
	  name varchar(255) COLLATE utf8_bin DEFAULT NULL COMMENT '项目名称',
	  itemkey varchar(50) COLLATE utf8_bin NOT NULL COMMENT '项目的标识',
	  gid int(11) NOT NULL DEFAULT '1' COMMENT '所属项目集的id号',
	  sumdelay int(11) DEFAULT '1' COMMENT '间隔时间(秒）',
	  PRIMARY KEY (id),
	  UNIQUE KEY itemkey (itemkey) USING BTREE
	) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='统计项目表';
	""" % items_mrk
	if items_mrk:
		res,desc = stat_db.query("show tables like 'stat_item_%s'" % items_mrk )
		if res==0 and not desc:
			rs,ds = stat_db.query(itesm_tabse_ddl,1)
			if rs== -1:
				return err_handle.db_err
			
	history_tabse_ddl = """
	  Create Table  stat_history_%s (
	  itemid bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '项目id号',
	  clock int(11) NOT NULL DEFAULT '0' COMMENT '数据产生时间',
	  val float(16,4) NOT NULL DEFAULT '0.0000' COMMENT '值',
	  gid int(11) DEFAULT '1' COMMENT '项目集id号',
	  KEY history_1 (itemid,clock) USING BTREE
	) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='存放统计数据';
	""" % history_mrk
	if 	history_mrk:
		res,desc = stat_db.query("show tables like 'stat_history_%s'" % items_mrk )
		if res==0 and not desc:
			rs,ds = stat_db.query(history_tabse_ddl,1)
			if rs ==-1:
				return err_handle.db_err
	return [0,gid]	

def get_groups(gkey=[]):
	"""提取group信息
	返回值:[status,info]
	status: 0 成功
			-1 gkey未设置
	        -100 数据库错误
	"""
	stat_db = mysqldb.get_db()
	item = {"table":"stat_item_group","fields":"*"}
	if  gkey and type(gkey) in (list,tuple):
		gk = ["'%s'" % k for k in gkey]
		item['where'] = "gkey in (%s)" % ",".join(gk)
	elif type(gkey) == str and gkey !='all' or not gkey:
		return err_handle.gkey_not_set
	res,desc = stat_db.query(item)
	if res == -1:
		return err_handle.db_err
	return res,desc

def update_group(gkey,data):
	"""更新
	"""
	stat_db = mysqldb.get_db()
	data.pop('gid')
	res,group = get_groups([gkey])
	if res == -1:
		return res,group
	if res ==0 and not group:
		return [-3,"%s 未注册."%gkey]
	if data:
		
		res,desc = stat_db.update("stat_item_group",data,"gkey='%s'" %gkey)
		if res ==0 and desc:
			#成功更新后检查是否有变更item表和history表
			if "items_mrk" in data and data['items_mrk'] != group['items_mrk'] \
			or "history_mrk" in data and data['history_mrk'] != group['history_mrk']:
				if "name" not in data:
					data['name'] = group['name']
				if "pid" not in data:
					data['pid'] = group['pid']
				reg_group(gkey,data)
				reg_items2redis(gkey)
			return res,desc
		elif res ==-1:
			return err_handle.db_err
		return [0,[]]
	else:
		return err_handle.data_not_found
		
		
#----------items操作----------#	
def reg_items(gkey,itm,prefix=''):
	"""注册items
	参数说明:
	gkey group的标识
	itm items组[[name,key]]
	prefix key的前缀
	
	"""
	#stat_db = dbclass(sconf.SYS['mysql'])	
	#stat_db.connect()
	stat_db = mysqldb.get_db()
	#取group信息
	res,desc = get_groups([gkey])
	if res==0 and desc:
		itm_tb = "stat_item_%s" % desc[0]['items_mrk'] if desc[0]['items_mrk'] else "stat_item"
		value = []
		for k in itm:
			value.append("('%s','%s%s',%s)" % (k[0],prefix,k[1],desc[0]['gid']))
		sql = "insert into %s (name,itemkey,gid)values %s " %(itm_tb, ",".join(value))
		res,desc = stat_db.query(sql,1)
		if res == -1:
			
			if desc[0] == 1062:
				return err_handle.item_exis
			return err_handle.db_err
		else:
			return [0,'']
	else:
		return res,desc

def get_items(gkey,item=[]):
	"""提取items
	"""
	stat_db = mysqldb.get_db()
	res,desc = get_groups([gkey])
	if res==0 and desc:
		itm_tb = get_itm_name(desc[0]['items_mrk'])
		sql_item={"table":itm_tb,"fields":"*",'where':"gid=%s"%desc[0]['gid']}
		if item:
			itms = ["'%s'" % k for k in item]
			sql_item['where']+=" and itemkey in (%s)" % ",".join(itms)
		res,desc = stat_db.query(sql_item)
		if res ==-1:
			return err_handle.db_err
		return [res,desc]
	else:
		return res,desc

def update_item_key(gkey,oldkey,newkey):
	stat_db = mysqldb.get_db()
	res,desc = get_groups([gkey])
	rdb = rediswrap.get_redis()
	if res==0 and desc:
		itm_tb = get_itm_name(desc[0]['items_mrk'])	
		res,des = stat_db.update(itm_tb,{"itemkey":newkey},"itemkey='%s'" % oldkey)
		if res ==0 and des:
			id = rdb.hget(RD_ITM_KEY_PRFX+gkey,oldkey)
			if id :
				rdb.hset(RD_ITM_KEY_PRFX+gkey,newkey,id)
		elif res == -1:
			return err_handle.db_err
		return res,des
	return res,desc
def update_item_name(gkey,itemkey,name):
	stat_db = mysqldb.get_db()		
	res,desc = get_groups([gkey])	
	if res==0 and desc:
		itm_tb = get_itm_name(desc[0]['items_mrk'])	
		res,desc = stat_db.update(itm_tb,{"name":name},"itemkey='%s'" % itemkey)
	if res ==-1 :
		return err_handle.db_err
	return res,desc
def get_itm_name(mrk):
	"""获取items表名
	"""
	return "stat_item_%s" % mrk if mrk else "stat_item"	
#-------------redis操作----------#		
def reg_items2redis(gkey,itm=[]):
	"""将items存入redis缓存
	"""
	rdb = rediswrap.get_redis()
	stat_db = mysqldb.get_db()
	hash_tb = rediswrap. get_hash(gkey, system='default',serialized_type='string')
	res,desc = get_groups([gkey])
	if res==0 and desc:
		itm_tb = get_itm_name(desc[0]['items_mrk'])
		rdb.hsetnx(RD_ITM_KEY_PRFX+gkey,'mrk',"%s,%s" %(desc[0]['items_mrk'],desc[0]['history_mrk']))
		gid = desc[0]['gid']
		
		i=0
		#设置了itemkey列表，依据itemkey取值
		if itm:
			itm_len = len(itm)
			while True:
				j = i+50 if i+50 < itm_len else itm_len 
				if i == itm_len:
					break
				key = ['"%s"' % k for k in itm[i:j]]
				sql = "select id,itemkey from %s where itemkey in (%s)" % (itm_tb, ",".join(key))

				res,desc = 	stat_db.query(sql)

				new_dict = {}
				if res ==0 and desc:
					for row in desc:
						new_dict[row['itemkey']]=row['id']
					rs = rdb.hmset(RD_ITM_KEY_PRFX+gkey,new_dict)
				i = j
		#未设置itemkey列表，依据gkey取出该组所有的items
		else:
			res, desc = stat_db.query("select min(id) as mnid,max(id) as mxid from %s where gid = %s" % (itm_tb,gid))

			mnid = desc[0]['mnid']
			mxid = desc[0]['mxid']
			limit = 50
			while True: 
				if mnid == mxid:
					break
				sql = "select id,itemkey from %s where id > %s and gid=%s limit %s" % (itm_tb,mnid,gid,limit)
				res,desc = 	stat_db.query(sql)
				
				new_dict = {}
				if res ==0 and desc:
					for row in desc:
						new_dict[row['itemkey']]=row['id']
						mnid = row['id']
					rdb.hmset(RD_ITM_KEY_PRFX+gkey,new_dict)	

def mod_redis_mrk(gkey,items_mrk,history_mrk):
	"""更改item在redis中的items_mrk,items_mrk
	"""
	rdb = rediswrap.get_redis()
	rdb.hsetnx(RD_ITM_KEY_PRFX+gkey,'mrk',"%s,%s" %(items_mrk,history_mrk))

def del_redis_items(gkey):
	"""删除item缓存
	"""
	rdb = rediswrap.get_redis()
	rdb.delete(RD_ITM_KEY_PRFX+gkey)
	
def send(gkey,data):
	"""在redis中缓存统计数据
	"""
	rdb = rediswrap.get_redis()
	keys = list(data.keys())
	ids = rdb.hmget(RD_ITM_KEY_PRFX + gkey,keys)
	if not ids:
		return [-7,"items not find in redis."]
	x = 0
	false_key=[]
	for i in range(0,len(ids)):
		if ids[i]:
			rdb.hincrby(RD_ITM_HST_TMP_PRFX+gkey,ids[i],data[keys[i]])
			x +=1 
		else:
			false_key.append(keys[i])
	return [0,x,false_key]
	
#--------------history操作--------#	
def get_hst_name(mrk):
	"""获取history表名
	"""
	return "stat_history_%s" % mrk if mrk else "stat_history"	
def set(gkey,data):
	"""上传值，先从redis缓存中取出item的id，再匹配itemkey入history库
	参数说明:
	gkey group 的gkey
	data 数据集 最好一次不要超过100个
	  {'itemkey':[值,生成时间默认为当前时间戳]}
	"""
	stat_db = mysqldb.get_db()
	rdb = rediswrap.get_redis()
	kys = list(data.keys())
	#加入表标识以确定目标表
	kys.append('mrk')
	itm = rdb.hmget(RD_ITM_KEY_PRFX+gkey,kys)
	itm_dict = {}
	if itm:
		mrk=itm.pop().split(',')
		hst_tb = get_hst_name(mrk[1])
		value = []
		for i in range(0,len(itm)):
			if itm[i] :
				tmp = data[kys[i]]
				clock = tmp[1] if tmp[1] else int(time.time())
				value.append("('%s','%s','%s')" %(itm[i],tmp[0],clock))
		if value:
			res,desc = stat_db.query("insert into %s(itemid,val,clock)values%s" % (hst_tb,','.join(value)),1)
			if res ==-1 :
				return [res,str(desc)]
			return res,desc
		else:
			return [-1,"no items find."]		
	return [-2,'items not in redis.']

			
def get(gkey,itm=[],start_time=0,stop_time=0,sort='clock asc',groupby=0,page=None):
	"""
	获取统计数据
	参数说明
	   itm itemid列表 为空时提取整个group的记录
	   start_time 开始时间戮
	   stop_time  结构时间戮
	   sort       排序方式 
	   groupby    分组方式 
	   page       分页参数集 {'site':每页数据量,'num':页码} 默认返回所有记录
	"""
	stat_db = mysqldb.get_db()
	rdb = rediswrap.get_redis()
	sql_item = {'fields':'*'}
	r_itmkey = RD_ITM_KEY_PRFX+gkey
	if itm:
		itm.append('mrk')
		itmids = rdb.hmget(r_itmkey,itm)
		mrk = itmids.pop().split(',')
		
	else:
		mrk = rdb.hget(r_itmkey,'mrk')
		itmids = rdb.hvals(r_itmkey)
		itmids.remove(mrk)
		mrk = mrk.split(',')	

	ids = [k for k in itmids if k ]	
	sql_item['table'] = get_hst_name(mrk[1]) 
	sql_item['where'] = " itemid in (%s) " % ",".join(ids)
	start_time = utils.timestamp(start_time) if start_time else utils.timestamp(0,'d')
	stop_time = utils.timestamp(stop_time) if stop_time else int(time.time())
	sql_item['where'] += " and clock>=%s and clock <%s" % (start_time,stop_time)
	sql_item['order'] = sort

	if groupby:
		if groupby ==1:
			sql_item['group'] = 'itemid'
		elif groupby == 2:
			sql_item['group'] = 'clock'
		else:
			sql_item['group'] = 'itemid,clock' 
		sql_item['fields'] = "itemid,sum(val) as val,clock"
	#分页这个mark一下。待定
	if page:
		s = page['num']*page['site']
		sql_item['limit'] = "%s,%s" %(s,page['site'])
	
	res,desc = stat_db.query(sql_item)
	#取得items的名称
	item_lab = {}
	if res == 0 and desc:
		itm_tb = "stat_item_" + mrk[0] if mrk[0] else "stat_item"
		rs, ds = stat_db.query("select name,id from %s where id in(%s)" %(itm_tb,",".join(ids) ))
		if rs==0 and ds:
			for row in ds :
				item_lab[row['id']]=row['name']
		return 0,[item_lab,desc]
	return 0,[{},[]]
		

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
		return 	get_cnf_val(host_key['info'],sconf.HOST)
	return None				
	

def sys_log(contxt):
	"""写入系统日志表
	"""
	stat_db = mysqldb.get_db()
	sql_item={'table':'stat_syslog','contxt':contxt}
				
	stat_db.query(sql_item)	
	
	
if __name__=="__main__":
	pass
		