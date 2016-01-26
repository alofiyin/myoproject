#_*_coding:utf-8_*_

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#工作注册模块
#$Id: async.py 649 2015-06-04 fiyin $#
__author__ = 'fiyin <alofiyin@gmail.com>'
__version__ = '$Revision: 0.1 $'

import types
import  system_info 

jobs_registry = {}
jobs_list = {}
def register(func, job_type='io', note='', func_name = None):
    """注册job
    参数说明
    =============
    job_type 类型
        io io密集型
        cup 计算密集型 
    note job功能说明
    """
    jobs_registry[func_name or func.__name__] = func
    jobs_list[func_name or func.__name__] = {'type':job_type, 'note':note}
def reg_job(*_args, **_kw):
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
        note = _kw.pop('note', '')
        register(handle, job_type, note)
    else:
        job_type = _kw.get('job_type', 'io')
        note = _kw.get('note', '')
        def _func(handle):
            register(handle, job_type, note)
        return _func

    
