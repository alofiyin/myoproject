#_*_coding:utf-8_*_

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#通过redis做为消息中枢获取指令,监听指令队列
#$Id: command_redis.py 649 2015-06-08 fiyin $#
__author__ = 'fiyin <alofiyin@gmail.com>'
__version__ = '$Revision: 0.1 $'
import config 
from rediswrap import *
from datamodel import *
import utils
import jobs_reg_mode
import os, time
import logging
from threading import Thread
import traceback
import global_list
#SERVER_NAME = 'wbsp'
#WORKNAME_NAME = ''
#LOCAL_IP = get_ip()
#DOING_TASKES={}
#G_EXIT = False
loger = logging.getLogger('worker.cmd_redis')
class CommandRedisThread(Thread):
	def __init__(self,cmd_queue):
		super(CommandRedisThread, self).__init__()
		self.cmd_queue = cmd_queue
			
	def run(self):
		commands = get_command_queue(global_list.WORKNAME_NAME)
		while True:
			if global_list.G_EXIT :
				loger.info("Thread exit....")
				os._exit(0)
				break
			try:
				command = commands.pop(timeout=5)
				
				if command :
					self.cmd_queue.put(command)
			except Exception as e:
				loger.error(str(e))