#_*_coding:utf-8_*_

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#
#$Id: model.py 649 2015-06-05 fiyin $#
g_exit = False
from rediswrap import get_set, get_key, set_key, \
get_queue, get_dict, get_keys, get_limit_queue, get_hash,expire,get_redis


def get_reg_list():
    """返回注册信息的哈希表
            返回类型:字典对象
    """
    key = "wbsp:worker:reg"
    return get_hash(key)
    
def set_online(name):
    """设置在线标识"""
    key = "wbsp:isonline.%s" % name
    set_key(key,'1', system='default',serialized_type='string')
    flush_online(name)  

def get_online_worker():
    """返回在线的工人"""
    workers = get_keys('wbsp:isonline.')
    wk = []
    for k in workers:
        if type(k) == bytes:
            k = k.decode()
        wk.append(k)
    return wk
    
def flush_online(name):
    """更新在线标识"""
    key = "wbsp:isonline.%s" % name
    expire(key,10,system='default')

def get_system_log_queue():
    """
    Json格式为:
    {'alias':'w01'
     'host':'192.168.1.100'
     'timestamp':123213123
     'type': 'reboot' or 'shutdown' or 'power' 三个值中其中一个
    }
    """
    system__log_queue ='wbsp:log:sys'
    return get_limit_queue(system__log_queue, 200)
    
def get_command_queue(name):
    """ 同步配置、状态报告、杀死转换线程
    
       要求同步worker配置
    {
     'command':'updateworker',
     'timestamp':''
                   }
        要求同步转换器线程驱动
    {
     'command':'updatedriver',
     'timestamp':''
                   }
                   
        要求worker报告整体工作状态::

     {
     'command':'report',
     'timestamp': 
     }
        后台杀一个转换进程（可能卡死）::
     {
     'command':'kill',
     'timestamp':
     'pid':'2121',
     }
    
    用户取消一个转换进程，和杀死类似，不应该进入错误队列，日志也需要说明是取消::
     {
     'command':'cancel',
     'timestamp':
     'pid':'2121',
     }
    """
    command_queue = 'wbsp:cmd.'+name
    return get_queue(command_queue)
    
def get_task_queue(name):
    """任务队列 提取任务
    Json格式为:
    {func:函数名,job_type:类型,pid:主任务编号,id:子任务编号,time:发布时间
    }
    """ 
    queue_name = 'wbsp:task.%s' % name
    return get_queue(queue_name)


def get_task_list():
    """返回主任务列表
    Json格式为:
    {func:函数名,job_type:类型,pid:主任务编号,time:发布时间,subtaskes:[子任务编号],
    }
    """ 
    queue_name = 'wbsp:task:list' 
    return get_hash(queue_name)

def get_task_hitory_list():
    """返回主历史任务列表
    Json格式为:
    {func:函数名,job_type:类型,pid:主任务编号,time:发布时间,subtaskes:[子任务编号],
    }
    """ 
    queue_name = 'wbsp:task:list:history' 
    return get_hash(queue_name)
def get_sub_hash():
    """
       子任务列
       Json格式为:
       { func:函数名,worker:工人编号,time:发布时间,runtime:运行时间,donetime:预计完成时间,status:状态,errinfo:出错信息
       }
    """
    name = 'wbsp:sub:tasks'
    return get_hash(name)

def get_sub_history_hash():
    """
       历史子任务列
       Json格式为:
       { func:函数名,worker:工人编号,time:发布时间,runtime:运行时间,donetime:完成时间,status:状态.
       }
    """
    name = 'wbsp:sub:tasks:history'
    return get_hash(name)
def clean_history():
	rdb = get_redis()
	rdb.delete("wbsp:sub:tasks:history")
	rdb.delete("wbsp:task:list:history")
	
def get_sys_err_queue():
    """
    错误日志
    Json格式为:
    {
    id:子任务编号,   pid:主任务编号   args:*参数,   keyword:**参数,   worker:工人编号,time:发布时间,runtime:运行时间, errinfo:出错信息
    }
    """
    name = "wbsp:log:error"
    return get_limit_queue(name, 200)
    
def get_cron_set():
    """ 定时任务list
    {id:任务编号,func:函数名,job_type:类型,time:发布时间,cron_info:定时,note:说明
          }
    """

    return get_set('wbsp:cron:task')    
    
def get_result_queue(pid):
    """
    取得保存任务执行结果的队列
    """
    name = "wbsp:result.%s" % pid
    return get_queue(name)          
    
def get_conn_hash():
    """数据服务连接信息
    Json格式为:
    {mysql:com: #连接标识 (数据库类型:数据库标识)
     {连接信息 服务器ip 端口 用户名 密码 等。。。}
     }
     
    """
    name = "wbsp:conn"
    return get_hash(name)
    
#--------------代理ip-----------
def get_tb_cache():
    """
    缓存表,保存生产表中测试已不可用的代理ip信息
    json格式:
    {ip:[port,type,trytime]}
    
    """
    return get_hash("wbsp:proxy.base")
def get_tb_prod():
    """
    #生产表,保存最新测试过可用的代理ip信息
    json格式:
    {ip:[port,type]}
    """
    return get_hash("wbsp:proxy.prod")  
def get_tb_temp():
    """
    临时表,保存采集回来的代理ip信息
    json格式:
    [ip,port,type]
    """
    return get_queue("wbsp:proxy.temp")  