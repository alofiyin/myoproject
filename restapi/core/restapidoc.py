#_*_coding:utf-8_*_
import docinfo
import sconf
import copy
import json
from pprint import pprint
API_DOC = docinfo.server_info



def get_doc():
	global API_DOC
	tags = []
	#----通用数据接操作----
	#注册api标签
	tag = docinfo.tags_style.copy()
	tag['name'] = "DBOperation"
	tag['description'] = "数据库通用写操作"
	API_DOC['tags'].append(tag)
	tags.append(tag['name'])
	#注册path
	itm = {}
	for k,v in docinfo.dbo_style['operation'].items():
		v['consumes'] = docinfo.consumes_style
		v['produces'] = docinfo.produces_style
		v['responses'].update(docinfo.responses_style)
		itm[k] = v
	API_DOC['paths'][docinfo.dbo_style['path']] = itm
	
	for k,v in docinfo.dbquery_style.items():
		v['get']['tags']	 = [tag['name']]
		v['get']['consumes'] = docinfo.consumes_style
		v['get']['produces'] = docinfo.produces_style
		v['get']['responses'].update(docinfo.responses_style)
		itm[k] = v
	API_DOC['paths'].update(itm)
	
	#搜索引擎操作
	tag = docinfo.tags_style.copy()
	tag['name'] = "search"
	tag['description'] = "搜索引擎查询"
	tags.append(tag['name'])
	API_DOC['tags'].append(tag)	
	itm = {}
	for k,v in sconf.DATA_SOURC['sphinx'].items():
		s_itm = copy.deepcopy(docinfo.sphinx_style['/search/{index}'])
		s_itm['get']['tags']	 = [tag['name']]
		s_itm['get']['consumes'] = docinfo.consumes_style
		s_itm['get']['produces'] = docinfo.produces_style
		s_itm['get']['responses'].update(docinfo.responses_style)
		s_itm['get']['summary'] = '%s%s' %(v['cname'],s_itm['get']['summary'])
		s_itm['get']['parameters']=s_itm['get']['parameters'][1:]
		inds = '/search/%s' % k
		itm[inds] = s_itm
	API_DOC['paths'].update(itm)

	#特殊查询业务
	itm = {}
	for k,v in docinfo.biz_api.items():
		v['get']['consumes'] = docinfo.consumes_style
		v['get']['produces'] = docinfo.produces_style
		v['get']['responses'].update(docinfo.responses_style)
		itm[k] = v	
	API_DOC['paths'].update(itm)
	#数据表通用操作
	itm = {}
	for k,v in docinfo.table_tag.items():
		for kk,vv in v.items():
			if vv['tag'] not in tags:
				tag = docinfo.tags_style.copy()
				tag['name'] = vv['tag']
				tag['description'] = vv['title']
				API_DOC['tags'].append(tag)
				tags.append(tag['name'])
			dbo_itm = {}
			#写操作
			for p, it in copy.deepcopy(docinfo.dbo_style['operation']).items():
				it['parameters']=it['parameters'][2:]
				it['tags'] = [vv['tag']]
				it['consumes'] = docinfo.consumes_style
				it['produces'] = docinfo.produces_style
				it['responses'].update(docinfo.responses_style)
				it['description'] = it['description'].replace('{dbname}',k).replace('{table}',kk)
				dbo_itm[p] =it 
			dbo_path =  docinfo.dbo_style['path'].replace('{dbname}',k).replace('{table}',kk)
			API_DOC['paths'][dbo_path] = dbo_itm

			#查询操作
			for pp,tt in copy.deepcopy(docinfo.dbquery_style).items():
				if pp.split('/')[-1] in vv['exception']:
					continue

				tt['get']['parameters']=tt['get']['parameters'][2:]
				tt['get']['tags'] = [vv['tag']]
				tt['get']['consumes'] = docinfo.consumes_style
				tt['get']['produces'] = docinfo.produces_style
				tt['get']['responses'].update(docinfo.responses_style)
				tt['get']['description'] = tt['get']['description'].replace('{dbname}',k).replace('{table}',kk)
				tt['get']['description']= "%s%s" %(tt['get']['description'],vv['description'])
				q_path = pp.replace('{dbname}',k).replace('{table}',kk)
				API_DOC['paths'][q_path] = tt
	body = json.dumps(API_DOC, indent=1)
	f = open('res.json','w')
	f.write(body)
	f.close()
