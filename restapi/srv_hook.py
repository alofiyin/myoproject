# -*- coding: utf-8 -*-

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#webapi勾子，读取传的biznum参数，获取配置信息
#调用执行程序
#$Id: contractio_servic.py 649 2015-06-12 fiyin $#
import cls_base
from  cls_base import get_cnf_val
import sconf
import traceback

#
#curl -l -H "Content-Type: application/json" -X POST -d  '{"biznum":"com.corp_targ","prama":{"tag_id":101,"lv2rows":13,"lv3rows":1}}'     http://192.168.10.126:6000/webapi/gettags
#
def hook(kw):
	biznum = kw.get('biznum','')
	if not biznum:
		return [-6,'parameter biznum not set.']
	#取业务配置
	bizcnf = get_cnf_val(biznum,sconf.BIZ)
	if not bizcnf:
		return sconf.err_handle.biznum_not_config	
	handle_name = bizcnf['handle']
	try:
		m,f = handle_name.split('.')
		exec("from ctl_%s import %s" % (m,f))
		handle = eval(f)
		kw['bizcnf'] = bizcnf
		rs = (handle(kw))
		#pprint(rs)
		return rs
	except Exception as e:
		print(traceback.format_exc())
		return [-101,'sys erro']