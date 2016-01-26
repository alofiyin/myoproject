#_*_coding:utf-8_*_
import re
import sys
import json
sys.path.append("%s/%s" % (sys.path[0][:-5],'modules'))
print(sys.path[0][:-5])
data = [
	{'prefix':'prod','split_table':'pro_info','databas':'biz72_product'}
	]
	
_import = """
#_*_coding:utf-8_*_
import gzip
import json
import time
from pprint import pprint
import logging
from sphinxwrap import sphinx
import sconf
from cls_base import *
import %s
import biz_tag as tagsclass

myaction = {}
#---------------
#数据接口
#---------------

""" 
insert = """
#表
@callback(myaction)
def %s_insert(prama):
	\"""插入一条公司记录
	参数:		
		data	dict	必填	mysql表数据集 {"字段名":"值", ....}
	返回内容:
		statusCode	int	状态码
		errInfo	string	错误说明
		insertId	int	入库id
	\"""
	return %s.%sinsert(prama)
"""

func = [insert]
def creat_code(data):
	for d in data:
		exec("import %s" % d['databas'])
		m = eval(d['databas']) 
		sql={'fields':'table_name','table':'information_schema.tables','where':"table_schema='%s' and table_type='base table'"%d['databas']}
		res,desc = m.query(sql)
		code = _import % d['databas']
		if res==0 and desc:
			for row in desc:
				if re.search('%s_\d+'%d['split_table'], row["table_name"]):
					continue
				
				if row["table_name"] == d['split_table']:
					pre = d['prefix']
				else:
					pre = ""
				#tb = row["table_name"].replace('_','')
				tb = fast_word_up(row["table_name"])
				for f in func:
					tmp = f % (tb,d['databas'],pre)
					code = "%s%s" % (code,tmp)
		print(code)
def fast_word_up(k):
	tmp = ["%s%s"%(s[0].upper(),s[1:]) for s in k.split('_')]
	return "".join(tmp)
				
if __name__ == "__main__":
#加载配置
	import sconf
	
	try:
	    sconf.SYS = json.loads("".join(open('../conf/sys.json').read().split()))
	except:
	    print("Erro: the file sys.json  is not json format, please check!\n system exit..")

	try:
	    sconf.HOST = json.loads("".join(open('../conf/host.json').read().split()))
	    sconf.DATA_SOURC = json.loads("".join(open('../conf/databases.json').read().split()))
	    #print(sconf.HOST)
	    #print(sconf.DATA_SOURC)
	except:
	    pass
	creat_code(data)