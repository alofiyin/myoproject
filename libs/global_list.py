#_*_coding:utf-8_*_
#全局变量

SERVER_NAME = 'wbsp'    #服务名前缀
WORKNAME_NAME = ''      #工人编号
LOCAL_IP = None     #本机IP
PROC_POOL = {}          #线程列表
DOING_TASKES={}         #正在进行的任务列表
G_EXIT = False          #全局退出标记

#任务执行状态说明
taskerr={
          'done':0,    #任务完成
          'doing':1,    #任务就绪
          'notjob':-1, #jobs.py中没有可以执行这个任务的函数
          'runerr':-2, #运行出错
          'runerr':-3, #工作站繁忙	
          'suspended':2,#任务暂停
        }

#任务状态 0 正常 1 暂停 2 取消
TASK_STAUS={}
