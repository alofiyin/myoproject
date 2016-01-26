#_*_coding:utf-8_*_
from cls_base import *
import sconf
import dbrest as dbhandle
from sphinxwrap import sphinx
from pprint import pprint
#
#搜索引擎操作
#

def parse(path):
	"""解析参数
		field:value;field:value
		field:1,2;
	"""
	result				={}
	result['intType']	= {}
	result['intRange']	= {}
	result['floatType']	= {}
	result['floatRange']= {}
	if not path:
		return result
	for f in path.split(';'):
		kv = f.split(':')
		if len(kv) < 2 :
			continue
		if '-' in kv[1]:
			numrange = kv[1].split('-')
			try:
				result['intRange'][kv[0]]="%s,%s,0" %(int(numrange[0]),int(numrange[1]))
			except:
				result['floatRange'][kv[0]]="%s,%s,0" % (numrange[0],numrange[1])
		else:
			numrange = kv[1].split('^')
			try:
				int(numrange[0])
				result['intType'][kv[0]]=",".join(numrange)
			except:
				result['floatType'][kv[0]]= ",".join(numrange)
	return result
	
def search(kw):
	"""提交搜索任务获取搜索结果及数据结果
	"""
	index = kw.get('index')
	host_info = sconf.get_search_info(index)
	kw['index'] = host_info['index']
	sp = sphinx(host_info['info']['host'],host_info['info']['port'])

	sp.initQuery(kw)
	rs = sp.RunQueries()
	result = {}
	if rs: 
		if  rs[0]['status']==0:
			result['total_found']	= rs[0]['total_found']
			result['total']			= rs[0]['total']
			result['time']			= rs[0]['time']
			
			ids			= []
			for row in rs[0]['matches']:
				if 'id' in row:
					ids.append(str(row['id']))
			if ids :
				dbinf			= {}
				dbinf['dbname'] = host_info['dbname']
				dbinf['table']	= host_info['table']
				dbinf['ids']	= ",".join(ids)
				dbinf['fields']	= kw.get('fields','*')
				if type(dbinf['fields']) in (tuple,list):
					if 'id' not in dbinf['fields']:
						dbinf['fields'].append('id')
					dbinf['fields'] = ','.join(dbinf['fields'])

				res,desc = dbhandle.getbyid(dbinf)
				if res == 0 and desc:
					rows = {str(row['id']):row for row in desc}
					result['data'] = [ rows[k] for k in ids if k in rows]
		else:
			result['warning'] = rs[0]['warning']
			result['error']	= rs[0]['error']
	else:
		return -1,sp._error
	return 0,result
				
	