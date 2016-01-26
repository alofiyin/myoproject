#_*_coding:utf-8_*_

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#命令执行类
#$Id: commandexecute.py 649 2015-06-04 fiyin $#
__author__ = 'fiyin <alofiyin@gmail.com>'
__version__ = '$Revision: 0.1 $'

import config 
import utils
import logging
import global_list
import os, time,sys
import jobs_reg_mode
from rediswrap import *
from datamodel import *
from threading import Thread

#SERVER_NAME = 'wbsp'
#WORKNAME_NAME = ''
#LOCAL_IP = get_ip()
#DOING_TASKES={}
#G_EXIT = False

logger = logging.getLogger('worker.command')

class CommandThread(Thread):
    """ 监视命令队列，取得命令, 执行命令"""

    def __init__(self,cmd_queue):
        super(CommandThread, self).__init__()
        self.login_time = int(time.time())
        self.cmd_queue = cmd_queue
        self.init()
        
    def init(self):
        #global SERVER_NAME, WORKNAME_NAME

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
            global_list.WORKNAME_NAME = wk_name
            reg_list = get_reg_list()   
            wk_info = reg_list.get(global_list.WORKNAME_NAME)
            if wk_info and wk_info['sysinfo']['ip'] == global_list.LOCAL_IP:
                return
        
        #global_list.WORKNAME_NAME = str(sum(map(lambda n:int(n),global_list.LOCAL_IP.split('.'))))
        global_list.WORKNAME_NAME = utils.get_mac()
        config.write('server','worker_name',global_list.WORKNAME_NAME)
        #合并线上配置
        reg_list = get_reg_list()
        wk_info = reg_list.get(global_list.WORKNAME_NAME)
        if wk_info and 'doing' in wk_info and wk_info['doing']:
            for k,task in wk_info['doing'].items():                
                if int(task['status']) < 3:
                    get_task_queue(global_list.WORKNAME_NAME).push(task)
        # 报告机器状态
        self.report(self.login_time)
        # 记录系统日志
        system_log = get_system_log_queue()
        system_log.push(dict( host=global_list.LOCAL_IP,
                        name=global_list.WORKNAME_NAME,
                        type='power',
                        timestamp=self.login_time))   
        #注册在线标识
        set_online(global_list.WORKNAME_NAME)   
    def report(self,timestamp=time.time()):
        """报告机器状态"""        
        reg_list = get_reg_list()
        sys_info = utils.get_sysinfo()
        job_list = jobs_reg_mode.jobs_list
        taks     = global_list.DOING_TASKES
        
        reg_list.__setitem__(global_list.WORKNAME_NAME,
                            dict(sysinfo=sys_info,
                            jobs_registry=job_list,
                            doing=global_list.DOING_TASKES,
                            uptime=timestamp))
        flush_online(global_list.WORKNAME_NAME)
        for k,v in taks.items():
            if int(v['status']) ==3:
                del global_list.DOING_TASKES[k]
    def result(self,handel):
        """返回结果
            预留用于兼容服务监听模式
        """
        pass    
        
        
    def run(self):
        global G_EXIT
        # 监听指令
        while True:
            
            if global_list.G_EXIT :
                break
            self.report(time.time())
            try:
                try:
                    command = self.cmd_queue.get(timeout=5)
                    if not command:
                        continue
                except:
                    continue
                logging.info("got command [%s]" % command)
                if command['command'] == 'report':
                    self.report()
                    
                elif command['command'] == 'exit':
                    global_list.G_EXIT = True
                    # TODO
                    #async_drive_config()
                    os._exit(0)

                    break
                elif command['command'] == 'updateworker' and \
                        CONFIG['server'].get('active_config', 'false').lower() == 'true':
                    queue = ztq_core.get_worker_config()
                    set_job_threads(queue[self.worker_name])
                elif command['command'] == 'kill':
                    kill_transform(pid=command['pid'], timestamp=command['timestamp'])
                elif command['command'] == 'cancel':
                    cancel_transform(pid=command['pid'], timestamp=command['timestamp'])
                else:
                    import _command
                    if command['command'] in dir(_command):
                        f=eval('_command.%s' %command['command'] )
                        res = f((),**command)
                        logger.info('"%s" "%s" "done"' % ("cmd",str(command)))
                    else:
                        logger.info('"%s" "%s" "命令不存在."' % ("cmd",str(command)))
            except ConnectionError as e:
                logger.error('ERROR: redis command connection error: %s' % str(e))
                time.sleep(3)
            except ResponseError as e:
                logger.error('ERROR: redis command response error: %s' % str(e))
                time.sleep(3)

            except KeyboardInterrupt:
                # 实际上调用的是command_execute.clear_thread
                os._exit(0)
            except Exception as e:
                logger.error('unknown error: %s' % str(e))
                time.sleep(3)
                
            