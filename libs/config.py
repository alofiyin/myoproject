#_*_coding:utf-8_*_

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#py3兼容
#$Id: config.py 649 2015-06-01 fiyin $#

import os 
try:
	from ConfigParser import ConfigParser
except ImportError:
	from configparser import  ConfigParser
# 读取配置文件（app.ini），保存到CONFIG中，实际使用的都是CONFIG
CONFIG = {}
CFG = None
def read(location):
    global CONFIG,CFG
    """ 初始化配置管理
    """
    CFG = ConfigParser()
    '''
    if location:
        cfg.read(location)
    else:
        local_dir = os.path.dirname(os.path.realpath(__file__))
        cfg.read( os.path.join(local_dir, 'config.cfg') )
    '''
    CFG.read(location)
    
    for section in CFG.sections():
        CONFIG[section] = {}
        for option in CFG.options(section):
            CONFIG[section][option] = CFG.get(section, option)
    return CONFIG


def write(section, option, value):
    CFG.set(section, option, value)
