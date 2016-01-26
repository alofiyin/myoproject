#_*_coding:utf-8_*_

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#工具类
#$Id: HttpWrap.py 649 2015-06-01 fiyin $#
from imp import reload
import time
import json
def str2hex(s,code='UTF-8'):
    """将字符串以16进制显示
    """
    return ''.join(list(map(lambda i:format(i,'x'),s.encode(code))))

def hex2str(s):
    """字节流转化
    a='我'.encode('utf_16_be')
    list(b) = [98, 17]
    c=bytes([98,17])
    b='我'.encode('utf_32_be')
    list(b) = [0, 0, 98, 17]
    c=bytes([0, 0, 98, 17])
    """
    
    pass
            
def get_sysinfo():
    """ 取得系统资源使用情况"""
    import system_info
    from multiprocessing import cpu_count
    info = {}
    info['cpu'] = (cpu_count(),int(round(float(system_info.get_cpu_usage()))),system_info.get_cpu_style())
    info['mem'] = system_info.get_mem_usage()
    info['ip'] = system_info.get_ip()
    return info 

def get_process_count(level):
    import system_info
    import multiprocessing 
    """根据级别和cpu数量来决定线程数
    @level_dist
        low 低使用率 10%cpu线程数 
        mid 中等使用率 50%cpu线程数
        high  高使用率 80%cpu线程数
        power   满负载   所有cpu线程数
    """
    
    level_dist = {'low':0.3,
                  'mid':0.5,
                  'high':0.8,
                  'power':1}
    #pdb.set_trace()                
    cpus = multiprocessing.cpu_count()
    usage = float(system_info.get_cpu_usage())*0.01
    cpu_free = cpus * (1 - usage)   
    pro_num = int(cpu_free * level_dist[level]) or  1
    
    return pro_num
    
def get_mac():
    """获取网卡的mac地址
    """
    import uuid
    node = uuid.getnode()
    mac = uuid.UUID(int = node).hex[-12:]
    return mac  

def write_file(fname,data):
    """写文件日志"""
    fp = open(fname,'wb')
    fp.writelines(data)
    fp.close()

def union_dict(*objs):  
    """
    字典合并
    如果key相同的话它们的值就相加。
    例：
    -----------
    d1={'a':10,'b':5}
    d2={'a':8,'b':10,'c':90}
    union_dict(d1,d2)
    result: {'a':18,'b':15,'c':90}
    """
    _keys = set(sum([list(obj.keys()) for obj in objs],[]))  
    _total = {}  
    for _key in _keys:  
        _total[_key] = sum([obj.get(_key,0) for obj in objs])  
    return _total
    
def dichotomy(L,K,Index=0):
    """二分法查找
    """
    if(len(L) in [0,1]):
        return Index

    length = int(len(L) / 2)
    
    hit = L[length]

    if(hit == K):
        return Index + length
    else:
        if hit > K:
            return dichotomy(L[:length],K,Index)
        else:
            return dichotomy(L[length + 1:],K,Index + length + 1)
                
def time_format(timesec=0,fromat='%Y-%m-%d %H:%M:%S'):
    """格式化时间戳
    """
    if not timesec:
        timesec = time.localtime()
    else:
        timesec = time.localtime(int(timesec))
    return time.strftime(fromat,timesec)

def timestamp(date=0,tail='s'):
    """获取时间戮
    date YYYY-mm-dd HH:MM:SS 格式 或者为时间戳
    tail 返回精度 [s 秒，[m 分[h小时[d 天]
    
    """
    if date == 0:
        date = int(time.time())
    if type(date) == str:
        try:
            t = list(time.strptime(date,'%Y-%m-%d %H:%M:%S'))
        except:
            t = list(time.strptime(date,'%Y-%m-%d'))
    else:
        t = list(time.localtime(date))
        
    if tail == 'm':
        t[5]=0
    elif tail == 'h':
        t[5]=t[4]=0
    elif tail == 'd':
        t[5]=t[4]=t[3]=0
    elif tail == 'M':
        t[5]=t[4]=t[3]=t[2]=0
    return int(time.mktime(tuple(t)))
    
class JSONEncoder(json.JSONEncoder):
    """
        处理理对像中有byter类型的情况:
            raise TypeError(repr(o) + " is not JSON serializable")
            TypeError: b'' is not JSON serializable
        
        调用方法JSONEncoder().encode(analytics)
    """
    def default(self, o):
        if isinstance(o, bytes):
            return o.decode()
        return json.JSONEncoder.default(self, o)
        


