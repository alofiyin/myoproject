# -*- coding: utf-8 -*-
#用于存放全局配置
import os
import logging
import json
logger = logging.getLogger('main')

PAGE_SIZE = 20
PAGE_SIZE_MAX = 1000

CONFIG={}
SYS={}
HOST={}
DATA_SOURC={
	'mysql_read':{},
	'mysql_write':{},
	'redis':{},
	'sphinx':{}
	}
	
BIZ={}
CNF_PATH='./conf'

class err_handle:
	loss_arg = [-6,'缺失参数']
	gkey_not_set = [-1,'未检测到参数gkey.']
	items_not_set = [-2,'未检测到参数items']
	db_err = [-100,'数据库操作错误']
	db_not_config = [-103,'data server not config']
	gkey_not_found = [-3,'gkey未注册']
	data_not_found = [-4,'未检测到参数data']
	item_exis = [-5,'item已存在']
	sphinx_param_not_set = [-10,"没有设置参数组param"]
	sphinx_index_not_found = [-11,'索引不存在']
	biznum_not_config = [-20,"biznum not config."]

def set_conf_path(path):
	"""设置配置文件目录
	"""
	global CNF_PATH
	CNF_PATH = path
	
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
        		
def load_sys_conf():
	global SYS
	"""加载系统配置sys.json
		读取cnf_path的json配置文件加载配置
	"""
	try:
		SYS = json.loads("".join(open('%s/sys.json'%CNF_PATH).read().split()))
	except:
		print("Erro: the file %s/sys.json  is not json format, please check!\n system exit.." % CNF_PATH)
		os._exit(0)
def load_host_conf():
	"""加载应用服务器配置
	"""
	global HOST
	try:
		HOST = json.loads("".join(open('%s/host.json'%CNF_PATH).read().split()))
	except:
		print("Erro: the file %s/host.json  is not json format, please check!\n system exit.." % CNF_PATH)
		os._exit(0)	
    	
def load_db_conf():
	"""加载数据源信息
	"""
	global DATA_SOURC
	try:
		data = json.loads("".join(open('%s/dbsource.json'%CNF_PATH).read().split()))
	except Exception as e:
		logger.error("config file %s/dbsource.json not load. please check."%CNF_PATH)
		return
	mysql = data.pop('mysql')
	data['mysql_read'] = mysql['read']
	data['mysql_write'] = mysql['write']
	for k,v in data.items():
		tmp = {}
		for kk, vv in v.items():
			vv['info'] = get_cnf_val(vv['info'],HOST)
			tmp[kk] = vv
		DATA_SOURC[k]=tmp

def get_db_info(name,readonly=True):
	"""获取msyql数据库服务器信息
	"""
	sinfo = DATA_SOURC['mysql_read'] if readonly else DATA_SOURC['mysql_write']
	if name and name in sinfo:
		info = sinfo[name]
		return info
	return None

def get_db_list(readonly=True):
	"""获取数据库标识列表
	"""
	if readonly : return list(DATA_SOURC['mysql_read'].keys())
	return list(DATA_SOURC['mysql_write'].keys())

def get_search_info(index):
	"""获取搜索引擎服务器信息
	"""
	return DATA_SOURC['sphinx'].get(index)

def get_search_list():
	"""获取搜索引擎索引列表
	"""
	return list(DATA_SOURC['sphinx'].keys()) 
		
def load_biz_conf():
	global BIZ
	for f in CNF_PATH:
	    try:
	        if f[:4]=='biz_' and f[-5:]=='.json':
	            BIZ[f[4:-5]] = json.loads(open("%s/%s"%(CNF_PATH,f)).read().replace('\n','').replace('\t',''))
	    except:
	        logger.error("config file %s/%s not load. please check."%(CNF_PATH,f))
	        
class swagger:
    """输出rest说明
    """
    def on_get(self,req,resp): 
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type, api_key, Authorization')
        #resp.set_header('Access-Control-Max-Age', 1728000)
        body = json.loads(open("%s/res.json"%CNF_PATH).read().replace('\n','').replace('\t',''))
        #body = open("%s/rest.json"%CNF_PATH).read()
        resp.body=json.dumps(body)