#_*_coding:utf-8_*_

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#任务注册模块
#$Id: async.py 649 2015-06-13 fiyin $#
__author__ = 'fiyin <alofiyin@gmail.com>'
__version__ = '$Revision: 0.1 $'

import types
import  system_info 


task_registry = {}
task_list = {}
def register(func, job_type='io', info='', func_name = None):
    """注册job
    参数说明
    =============
    job_type 类型
        io io密集型
        cup 计算密集型 
    note job功能说明
    {'alias':别名,'args':参数示例,'note'：功能简介}
    """
    task_registry[func_name or func.__name__] = func
    task_list[func_name or func.__name__] = {'type':job_type, 'info':info}
def reg_task(*_args, **_kw):
    """ 这是一个decorator,本地注册job
    定义job
    ==============
        @regJob(job_type='io',note='这是一个测试程序')
        def say_hello(name):
            print 'hello, ', name
    """
    if len(_args) ==1 and not _kw and isinstance(_args[0], types.FunctionType):
        handle= _args[0]
        job_type = _kw.pop('job_type', 'io')
        info = _kw.pop('info', '')
        register(handle, job_type, info)            
    else:
        _model = _kw.pop('model','')
        job_type = _kw.get('job_type', 'io')
        info = _kw.get('info', '')
        def _func(handle):
            register(handle, job_type, info)
            def _exe(*args,**kw):
                pass
                '''
                if not _model:
                    return
                model = "modules.%s" % _model
                print(model)
                if _model in dir():
                    reload(model)
                else:
                    __import__(model)
                '''
            _exe.__raw__= handle
            return _exe
        return _func

    
