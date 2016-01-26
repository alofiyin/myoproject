# -*- coding: utf-8 -*-

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#服务程序
#$Id: contractio_servic.py 649 2015-06-12 fiyin $#

from eventlet_srvd import ENTService
import logging
import pdb,time
import traceback
import eventlet
import json
from utils import JSONEncoder

from httpparse import HttpParse

logger = logging.getLogger('main')

eventlet.monkey_patch()

class PMService(ENTService):
    def __init__(self):
        super(PMService, self).__init__()
        self._port = 1983
              
    def handle(self,client):
        """
        """
        t=float('%0.3f'%time.time())
        try:
            #pdb.set_trace()
            new_sock ,addr = client
            res = new_sock.recv(2048)
            path=""
            try:        
                html = HttpParse(res)
                path = html._Header['Request']
                if html._Header['Method']=='POST':
                    body_len = int(html._Header['content-length'])
                    if len(html._DATA) < body_len:
                        while 1:
                            c = new_sock.recv(512)
                            html._DATA = html._DATA + c
                            if len(html._DATA) >= body_len:
                                break

                    if 'content-type' in html._Header and html._Header['content-type'].find('multipart/form-data') >-1:
                        html._parse_multipart()
                    else:
                        html._parse_post()    
            except Exception as e:
                traceback.print_exc()
                raise Exception('The request of the error')
            #路由解析
            try:
                mod, func = html.getpath()[:2]
            except:
                h = 'HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK'
                new_sock.send(h.encode())
                new_sock.close()
                return
                   
            kw  = html._GET or html._POST or html.Up_File or html._DATA or {}
            #print(kw)
            rs = ""
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
                logger.info('"%s" "%s" "cmd"' % (addr[0],path) )
            else:             
                try:
                    if type(kw) != dict:
                        rs = "[-102,'data body not json format.'"
                    else:
                        exec("from ctl_%s import %s" % (mod, func))
                        f = eval(func)
                        #rs = json.dumps(f(kw))
                        rs = JSONEncoder().encode(f(kw))
                    
                except Exception as e:
                    #raise e
                    traceback.print_exc()
                    rs = "[-101,'sys erro']"
            ftime = float('%0.3f'%(time.time()-t))
            logger.info('"%s" "%s" "%s"' % (addr[0],path,ftime) )
            h = 'HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK'
            
            if rs:
                h = 'HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s' % (len(rs),rs)

            new_sock.send(h.encode())
            new_sock.close()
            
            self._report += 1
        except Exception as e:
            traceback.print_exc()
            errinfo = traceback.format_exc()
            #errinfo='出错了'
            #logger.error('"%s" "%s" "erron" "%s"' % (addr[0],path,errinfo))
            req = 'HTTP/1.1 500 system error!\r\nContent-Length: %d\r\n\r\n%s' % (len(str(e)),str(e))
            #req = 'HTTP/1.1 500 system error!\r\n\r\n'
            new_sock.send(req.encode())
            new_sock.close()
        #service.__soketset.remove(clinet)
