#_*_coding:utf-8_*_

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#命令执行类
#$Id: commandexecute.py 649 2015-06-04 fiyin $#
__author__ = 'fiyin <alofiyin@gmail.com>'
__version__ = '$Revision: 0.1 $'

import config 
from rediswrap import *
from datamodel import *
import utils
import jobs_reg_mode
import os, time
import logging

#SERVER_NAME = 'wbsp'
#WORKNAME_NAME = ''
#LOCAL_IP = get_ip()
#DOING_TASKES={}
#G_EXIT = False
class CommandThread(Thread):
	""" 监视命令队列，取得命令, 执行命令"""

    def __init__(self,cmd_queue):
        super(CommandThread, self).__init__()
        self.login_time = int(time.time())
		self.cmd_queue = cmd_queue
    def init(self):
    	#global SERVER_NAME, WORKNAME_NAME
    	global  WORKNAME_NAME
        """ 办理工人注册 """
        #srv_name = config.CONFIG['server']['server_name']
        wk_name =  config.CONFIG['server']['worker_name']
        """检测配置文件
        if srv_name: 
        	SERVER_NAME = srv_name
        else:
        	config.write('server', 'server_name', SERVER_NAME)
        """
        if wk_name: 
        	WORKNAME_NAME = wk_name
        	reg_list = get_reg_list()	
        	wk_info = reg_list.get(WORKNAME_NAME)
        	if wk_info and wk_info['sysinfo']['ip'] == LOCAL_IP:
        		return
        
        WORKNAME_NAME = sum(map(lambda n:int(n),LOCAL_IP))
        config.write('server','worker_name',WORKNAME_NAME)
        # 报告机器状态
        self.report(self.login_time)
        # 记录系统日志
        system_log = get_system_log_queue()
 		system_log.push(dict( host=LOCAL_IP,
						name=WORKNAME_NAME,
						type='power',
						timestamp=self.login_time))   
		#注册在线标识
		set_online(WORKNAME_NAME)   
	def report(self,timestamp=time.time()):
        """报告机器状态"""		
        reg_list = get_reg_list()
        sys_info = utils.get_sysinfo()
        job_list = jobs_reg_mode.jobs_list
        #taks     = worker.doing_taks
        
        reg_list.__setitem__(WORKNAME_NAME,
        					dict(sysinfo=sys_info,
        					jobs_registry=job_list,
        					doing=DOING_TASKES,
        					uptime=timestamp))
		flush_online(WORKNAME_NAME)
		
    def run(self):
    	global G_EXIT
        self.init()
        # 监听指令
        commands = get_command_queue(WORKNAME_NAME)
        while True:
        	if G_EXIT :
        		break
            try:
                command = commands.pop(timeout=5)
                if command['command'] == 'report':
                    self.report()
                    
                elif command['command'] == 'exit':
                	G_EXIT = True
                    # TODO
                    #async_drive_config()
                    break
                elif command['command'] == 'updateworker' and \
                        CONFIG['server'].get('active_config', 'false').lower() == 'true':
                    queue = ztq_core.get_worker_config()
                    set_job_threads(queue[self.worker_name])
                elif command['command'] == 'kill':
                    kill_transform(pid=command['pid'], timestamp=command['timestamp'])
                elif command['command'] == 'cancel':
                    cancel_transform(pid=command['pid'], timestamp=command['timestamp'])
            except ztq_core.ConnectionError, e:
                logger.error('ERROR: redis command connection error: %s' % str(e))
                time.sleep(3)
            except ztq_core.ResponseError, e:
                logger.error('ERROR: redis command response error: %s' % str(e))
                time.sleep(3)

            except KeyboardInterrupt:
                import os
                # 实际上调用的是command_execute.clear_thread
                os.sys.exitfunc()
                os._exit(0)
            except Exception, e:
                logger.error('ERROR: redis command unknown error: %s' % str(e))
                time.sleep(3)
                
			self.report()