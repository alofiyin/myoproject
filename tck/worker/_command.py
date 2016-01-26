# -*- coding: utf-8 -*-

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#工作站命令集
#$Id: _command.py 649 2015-08-11 fiyin $#

from rediswrap import *
from datamodel import *
import global_list
import logging

def task_status(*ag, **kw):
	"""改变任务执行状态
	@status 
		0 恢复
		1 暂停
		2 取消
	@id 任务号 
	"""
	note = {0:'恢复',1:'暂停',2:'取消'}
	id 		= kw.pop('id')
	status  = int(kw.pop('status'))
	if id not in global_list.DOING_TASKES:
		return 

	task = global_list.DOING_TASKES[id]
	task['status'] = status+1
	get_sub_hash().set(task['id'],task)

