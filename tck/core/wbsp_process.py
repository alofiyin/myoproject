#_*_coding:utf-8_*_

# Copyright	(c)	2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#进程模版
#$Id: wbsp_process.py	649	2015-06-08 fiyin $#
__author__ = 'fiyin	<alofiyin@gmail.com>'
__version__	= '$Revision: 0.1 $'

import eventlet
import multiprocessing
import global_list
from system_info import	get_cpu_usage
import os, time, types, pdb
from threading import Thread

def	get_process_count(level):
	"""根据级别和cpu数量来决定线程数
	@level_dist
		low	低使用率 10%cpu线程数 
		mid	中等使用率 50%cpu线程数
		high  高使用率 80%cpu线程数
		power	满负载	  所有cpu线程数
	"""
	
	level_dist = {'low':0.3,
				  'mid':0.5,
				  'high':0.8,
				  'power':1}
	#pdb.set_trace()				
	cpus = multiprocessing.cpu_count()
	usage = float(get_cpu_usage()[:-1])*0.01
	cpu_free = cpus	* (1 - usage)	
	pro_num	= int(cpu_free * level_dist[level]) or	1
	
	return pro_num

def	process_exe(handle,proc_num, args=(), kw={}):
	"""
	进程运行函数
	"""

	#单进程
	if proc_num <=1:
		p = multiprocessing.Process(target=handle,	args=args,kwargs=kw)
		p.daemon = True
		p.start()
	#进程池
	else:
		pool = multiprocessing.Pool(processes=proc_num)
		for	i in range(0,proc_num):
			pool.apply_async(handle,*args, **kw)
		pool.close()
			
	
def	thread_exe(handle,size, *args, **kw):
	"""
	线程运行函数
	"""
	pool = eventlet.GreenPool(size)
	for	i in xrange(0,size):
		pool.apply_async(handle,*args, **kw)
	pool.close()			

class WBProcess(Thread):
	"""
		@_proc_num 进程数
		以_proc_num优先
	"""
	
	def __init__(self):
		super(WBProcess, self).__init__()
		self._proc_num = 1
		self._proc_info = {}
		self.exit_flag = multiprocessing.Event()
		
	def set_proc_num(self, proc_num):
		self._proc_num = proc_num
		
	def get_proc_num(self):
		return self._proc_num	
		
	def set_level(self, level):
		"""设置运行级别，由系统来决定进程数
			@level in [low, mid, high, power]
		"""
		self._proc_num = get_process_count(level)
		

	def proc_run(self, handle,proc_run=0, *args, **kw):
		proc_run = proc_run or self._proc_num
		process_exe(handle, proc_run, *args, **kw)
		
	
	def thread_run(self, size,handle, *args, **kw):
		thread_exe(handle,size, *args, **kw)

	def proc_pool(self):
		return multiprocessing.Pool(processes=self._proc_num)
		
	def thead_pool(self,size=100):
		return  eventlet.GreenPool(size) 
		
	def Queue(self):
		return multiprocessing.Queue()  
		
	def close(self):
		self.exit_flag.set()	