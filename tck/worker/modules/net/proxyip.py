#_*_coding:utf-8_*_

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#自动采集代理ip
#$Id: wordsfordb.py 649 2015-08-21 fiyin $#
from lxml import etree
from eventlet.green.urllib import request
from eventlet.green import socket 
import eventlet
from rediswrap import *
import jobstatus 
import multiprocessing as mp 
from datamodel import *
import logging
logger = logging.getLogger('worker.proxyip')

#eventlet.monkey_patch()



def test_proxy_ip(ip,port,_type='http'):
    """代理ip有效性检测
    参数说明:
    @ip     代理ip
    @port   代理端口号
    @type   代理类型 http https socket 此模块只收集http代理
    返回结果:
    (ip,port,type)   输入的代理信息
    flag  False 不可用 , True 可用
    """
    flag = False
    try:
        socket.setdefaulttimeout(10)
        proxy_handler = request.ProxyHandler({_type.lower():ip+':'+port})
        #proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
        #proxy_auth_handler.add_password('realm', '123.123.2123.123', 'user', 'password')

        opener = request.build_opener(proxy_handler)
        f = opener.open('http://14.17.127.67:81/t.php') 
        resip  = f.read().decode()
        if ip == resip:
            flag = True
    except Exception as e:
        #print(e)
        pass
    return (ip,port,_type),flag

def proxy_check_tmp(host):
    """批量检测临时表中代理ip有效性
       如有效则放入生产表
    """
    pool     = eventlet.GreenPool(50) #协程池
    tb_prod  = get_tb_prod()           #生产表
    tb_temp  = get_tb_temp()           #临时表
    ip_arg   = []                      #参数ip
    port_arg = []                      #参数端口
    type_arg = []                      #参数代理类型
    tmpip    = tb_temp.__len__()
    newip    = 0
    while 1: 
        try:
            row = tb_temp.pop(1)
            if not row:
                break
            ip_arg.append(row[0])
            port_arg.append(row[1])
            type_arg.append(row[2])
        except:
            pass
    for res,flag in pool.imap(test_proxy_ip,ip_arg,port_arg,type_arg):
        if flag and not tb_prod.get(res[0],False):
            newip+=1
            tb_prod.set(res[0],(res[1],res[2]))
    logger.info("proxy_check_tmp temp host:%s; ip_count:%s; add_ip_count:%s" %(host,tmpip,newip))      

def _proxy_check_prod(kw):
    """批量检测生产表中代理ip有效性
       如失效则移入缓存表
    """ 
    pool     = eventlet.GreenPool(50) #协程池
    tb_prod  = get_tb_prod()           #生产表
    tb_cache = get_tb_cache()          #缓存表
    ip_arg   = []                      #参数ip
    port_arg = []                      #参数端口
    type_arg = []                      #参数代理类型
    ip       =  tb_prod.__len__()       
    dieip    = 0
    for k,row in tb_prod.items():
        ip_arg.append(k)
        port_arg.append(row[0])
        type_arg.append(row[1])
    
    for res,flag in pool.imap(test_proxy_ip,ip_arg,port_arg,type_arg):
        if not flag:
            dieip+=1
            tb_cache.set(res[0],(res[1],res[2],1))
            tb_prod.__delitem__(res[0])
    logger.info("proxy_check_prod  ip count %s;die ip count %s" %(ip,dieip))

def _clean(kw):
    """批量检测缓存表中代理ip有效性
       如无效则trytime+1，如果trytime>5 刚清除
       如有效则移入生产表
    """     
    pool     = eventlet.GreenPool(50) #协程池
    tb_prod  = get_tb_prod()           #生产表
    tb_cache = get_tb_cache()          #缓存表
    ip_arg   = []                      #参数ip
    port_arg = []                      #参数端口
    type_arg = []                      #参数代理类型
    trytime  = {}
    ipcount  = tb_cache.__len__()
    saveip   = 0    
    for k,row in tb_cache.items():
        ip_arg.append(k)
        port_arg.append(row[0])
        type_arg.append(row[1])
        trytime[k]=row[2]

    if ip_arg:
        for res,flag in pool.imap(test_proxy_ip,ip_arg,port_arg,type_arg):
            if not flag:
                tn = trytime[res[0]] +1
                if tn >5:
                    tb_cache.__delitem__(res[0])
                else:
                    tb_cache.set(res[0],(res[1],res[2],tn))
            else:
                saveip +=1
                tb_cache.__delitem__(res[0])
                tb_prod.set(res[0],(res[1],res[2])) 
    logger.info("clean  ip count %s;save ip count %s" %(ipcount,saveip))
            
"""代理ip采集"""
def get_xici_proxy():
    """提取xici.net公布的代理ip
    """
    url=[]
    tb_temp  = get_tb_temp()
    pool = eventlet.GreenPool(2)
    for i in range(1,20):
        url.append('http://www.xici.net.co/nn/%s'%i)
    for html in pool.imap(request.urlopen,url):
        try:

            tree = etree.HTML(html.read().decode())
            for item in tree.xpath('//tr[@class="odd"]'):
                node = item.xpath('td')
                ip   = node[2].text
                port = node[3].text
                _type = node[6].text
                tb_temp.push((ip,port,_type.lower()))
        except Exception as e:
            #print(e)
            pass
    proxy_check_tmp("xici.net")

def get_cn_proxy():
    """提取cn-proxy.com公布的代理ip
    """
    tb_temp  = get_tb_temp()
    url="http://cn-proxy.com/"
    html = request.urlopen(url).read()
    tree = etree.HTML(html)
    tb  = tree.xpath('//tr')
    for item in tb:
        node = item.xpath('td')
        if node and node[0].text.find('.') >0:
            ip   = node[0].text
            port = node[1].text
            _type = 'http'
            tb_temp.push((ip,port,_type))
    proxy_check_tmp('cn-proxy.com')
def get_kuaidaili_proxy():
    """提取kuaidaili.com公布的代理ip
    """
    tb_temp  = get_tb_temp()
    for i in range(1,11):
        url="http://www.kuaidaili.com/proxylist/%s/" % i
        html = request.urlopen(url).read()
        tree = etree.HTML(html)
        tb  = tree.xpath('//tr')
        for item in tb:
            node = item.xpath('td')
            if node and node[0].text.find('.') >0:
                ip   = node[0].text
                port = node[1].text
                _type = 'http'
                tb_temp.push((ip,port,_type))
    proxy_check_tmp(kuaidaili.com)


def _get_proxy(kw):
    """获取代理ip
    """
    urls = kw.pop("urls",[])
    tb_temp  = get_tb_temp()
    if urls:
        for url in urls:
            try:
                res = request.urlopen(url).read().decode()
                for ip in res.split('\r\n'):
                    try:
                        ip,port = ip.split(':')
                        _type = 'http'
                        tb_temp.push((ip,port,_type))
                    except:
                        pass
                proxy_check_tmp(request.urlparse(url).netloc)
            except:
                pass
            
    func =[get_xici_proxy,get_cn_proxy,get_kuaidaili_proxy]
    for f in func:
        try:
            res = f()
        except:
            pass


"""---------------"""   

"""对外接口"""

def proxy_check_prod(kw):
    p = mp.Process(target=_proxy_check_prod, args=(kw,))
    p.daemon = True
    p.start()
    p.join()
    #任务执行完成调用结束函数报告状态 
    jobstatus.done(kw['id'])   

def clean(kw):
    p = mp.Process(target=_clean, args=(kw,))
    p.daemon = True
    p.start()
    p.join()
    #任务执行完成调用结束函数报告状态 
    jobstatus.done(kw['id'])   
    
def get_proxy(kw):
    p = mp.Process(target=_get_proxy, args=(kw,))
    p.daemon = True
    p.start()
    p.join()
    #任务执行完成调用结束函数报告状态 
    jobstatus.done(kw['id'])  
    
if __name__ == "__main__":
    setup_redis("default", '192.168.10.126', 6380)
    get_proxy()    
    #proxy_check_tmp()
