# -*- coding: utf-8 -*-

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#服务程序
#$Id: contractio_servic.py 649 2015-06-12 fiyin $#

from sokeSrv import ENTService
import logging
import pdb,time
import traceback


from httpparse import HttpParse

logger = logging.getLogger('main')


class PMService(ENTService):
    def __init__(self):
        super(PMService, self).__init__()
        self._port = 1983
        self.pm_pool = mp.Pool(5)
    def handle(self,client):
        body = b""
        try:
            new_sock ,addr = client 
            
            while 1:
                res = new_sock.recv(2048)
                if res:
                    body = body + res
                if not res or res[-4:] == b'\r\n\r\n':
                    break
                
        except:
            traceback.print_exc()
            pass
        res = self.pm_pool.apply_async(action,[body]).get()
        new_sock.send(res.encode())
        new_sock.close()     
def action(body):
    """
    """
    t=float('%0.3f'%time.time())
    try:
        path=""
        try:        
            html = HttpParse(body)
            path = html._Header['Request']
            if html._Header['Method']=='POST':
                body_len = int(html._Header['Content-Length'])
                if 'Content-Type' in html._Header and html._Header['Content-Type'].find('multipart/form-data') >-1:
                    html._parse_multipart()
                else:
                    html._parse_post()    
        except Exception as e:
            raise Exception('The request of the error')
        #路由解析
        try:
            mod, func = html.getpath()[:2]
        except:
            h = 'HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK'
            return h
               
        kw  = html._GET or html._POST or html.Up_File or html._DATA or {}
        if mod == 'cmd': 
            if func == 'reload_tasks':
                reload_tasks()
            elif func == 'reload_cmd':
                reload_cmd()
            else:
                models = dir(commands_)
                if func in models:
                    f = eval('commands_.%s' % func)
                    rs = json_dumps(f(kw))
            logger.info('"%s" "%s" "cmd"' % ("",path) )
        else:             
            try:
                exec("from %s import %s" % (mod, func))
                f = eval(func)
                rs = json.dumps(f(kw))
                
            except Exception as e:
                #raise e
                traceback.print_exc()
        ftime = float('%0.3f'%(time.time()-t))
        logger.info('"%s" "%s" "%s"' % ("",path,ftime) )
        #h = 'HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK'
        
        if rs:
            h = 'HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s' % (len(rs),rs)
        return h
        
        self._report += 1
    except Exception as e:
        traceback.print_exc()
        errinfo = traceback.format_exc()
        #errinfo='出错了'
        #logger.error('"%s" "%s" "erron" "%s"' % (addr[0],path,errinfo))
        req = 'HTTP/1.1 500 system error!\r\nContent-Length: %d\r\n\r\n%s' % (len(str(e)),str(e))
        #req = 'HTTP/1.1 500 system error!\r\n\r\n'
        return req
    #service.__soketset.remove(clinet)
