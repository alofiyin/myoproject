# -*- coding: utf-8 -*-
#用于存放全局配置
CONFIG={}
SYS={}
HOST={}
DATA_SOURC={}
BIZ={}
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
	
