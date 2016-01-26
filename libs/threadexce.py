#_*_coding:utf-8_*_

# Copyright	(c)	2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#进程、协程模版
#$Id: threadexce.py	649	2015-06-08 fiyin $#
__author__ = 'fiyin	<alofiyin@gmail.com>'
__version__	= '$Revision: 0.1 $'


import eventlet
import multiprocessing
from system_info import	get_cpu_usage
import os, time, types, pdb

#---------------------多进程表修饰符--------------------
def	get_process_count(level):
	"""根据级别和cpu数量来决定线程数
	"""
	level_dist = {'low':0.3,
				  'middle':0.5,
				  'high':0.8,
				  'power':1}
	#pdb.set_trace()				
	cpus = multiprocessing.cpu_count()
	usage = float(get_cpu_usage()[:-1])*0.01
	cpu_free = cpus	* (1 - usage)	
	pro_num	= int(cpu_free * level_dist[level]) or	1
	print (cpus,usage,cpu_free,pro_num)
	return pro_num
	
	
def	_process_exe(handle, _mode,	_pro_num, *args, **kw):
	"""
	进程运行函数
	"""
	print(args, kw)
	mode = kw.pop('mode', _mode)
	pro_num	= kw.pop('pro_num',	_pro_num)
	pro_num	= pro_num or get_process_count(mode)
	print('pro_num',pro_num)
	print (handle)
	#单进程
	if pro_num == 1:
		p = multiprocessing.Process(target=handle,	args=args,kwargs=kw)
		p.start()
	#进程池
	else:
		pool = multiprocessing.Pool(processes=pro_num)
		for	i in xrange(0,pro_num):
			pool.apply_async(handle,*args, **kw)
		pool.close()		
			
def	process_exe(*_args,**_kw):
	"""这是一个decorator，初始化进程
	@level string 设定线程数级别，由程序根据级别和cpu数量来决定线程数
		low	低使用率 10%cpu线程数 
		mid	中等使用率 50%cpu线程数
		high  高使用率 80%cpu线程数
		power	满负载	  所有cpu线程数
	@pro_num int 线程数
	
	@level与@pro_num二选一，只有一个有效，以@pro_num优先

	定义执行程序
	=============
	第一种::

		@process_exe
		def	say_hello(name):
			print 'hello, ', name

	第二种, 预先指定队列执行信息::
		@process_exe(level='mid')
		def	say_hello(name):
			print 'hello, ', name

		@process_exe(pro_num=4)
		def	say_hello(name):
			print 'hello, ', name
	使用方法
	================
	支持如下几种::

		say_hello('asdfa')
		say_hello('asdfa', pro_num=4)
		say_hello('asdfa', level='power')
	"""
	_mode =	'low'
	_pro_num = 0
	if len(_args) ==1 and not _kw and isinstance(_args[0], types.FunctionType):
		handle=	_args[0]
		def	_exe(*args,	**kw):
			print(args, kw)
			_process_exe(handle,_mode, _pro_num, *args,	**kw)		
		_exe.__raw__ = 	handle
		return _exe
	else:
		_md	= _kw.get('mode',_mode)
		_pro_num = _kw.get('pro_num', _pro_num)
		def	_func(handle):
			def	_exe(*args,	**kw):
				_process_exe(handle,_mode, _pro_num, *args,	**kw)
			_exe.__raw__= handle
			return _exe
		
		return _func		
	

#---------------------多线程表修饰符--------------------

def	_thred_exe(pool,handle,	*args, **kw):
	"""
	线程运行函数
	"""	
	pool.spawn(handle, *args, **kw)
		
def	thred_exe(*_args,**_kw):
	"""这是一个decorator，初始化线程

	@poolsize int 默认值100
	
	定义执行程序
	=============
	第一种::

		@thred_exe
		def	say_hello(name):
			print 'hello, ', name

	第二种, 预先指定队列执行信息::
		@thred_exe(poolsize='mid')
		def	say_hello(name):
			print 'hello, ', name
			
	使用方法
	================
	支持如下几种::

		say_hello('asdfa')
		say_hello('asdfa', poolsize=4)

	"""
	_poolsize =	100
	if len(_args) ==1 and not _kw and isinstance(_args[0], types.FunctionType):
		handle=	_args[0]

		pool = eventlet.GreenPool(_poolsize)
		def	_exe(*args,	**kw):
			_thred_exe(pool,handle,	*args, **kw)			
		return _exe
	else:
		_poolsize =	_kw.get('poolsize',_poolsize)
		pool = eventlet.GreenPool(_poolsize)
		def	_func(handle):
			def	_exe(*args,	**kw):
				_thred_exe(pool,handle,	*args, **kw)
			_exe.__raw__= handle
			return _exe
		return _func		
	
