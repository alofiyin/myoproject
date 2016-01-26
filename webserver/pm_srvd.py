# -*- coding: utf-8 -*-

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#工头服务程序
#$Id: contractio_servic.py 649 2015-06-12 fiyin $#

from eventlet_srvd import ENTService
import logging
import pdb,time
import traceback
import eventlet
import json
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
        
        try:
            #pdb.set_trace()
            new_sock ,addr = client
            res = new_sock.recv(2048)
            path=""

            try:        
                html = HttpParse(res)
                path = html._Header['Request']
                if html._Header['Method']=='POST':
                    body_len = int(html._Header['Content-Length'])
                    if len(html._DATA) < body_len:
                        while 1:
                            c = new_sock.recv(512)
                            html._DATA = html._DATA + c
                            if len(html._DATA) >= body_len:
                                break

                    if 'Content-Type' in html._Header and html._Header['Content-Type'].find('multipart/form-data') >-1:
                        html._parse_multipart()
                    else:
                        html._parse_post()    
            except Exception as e:
                raise Exception('The request of the error')
            #取得path前两级赋值予 模块名，函数名
            mod, func = html.getpath()[:2]
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
                logger.info('"%s" "%s" "cmd"' % (addr[0],path) )
            else:             
                try:
                    exec("from %s import %s" % (mod, func))
                    f = eval(func)
                    rs = json.dumps(f(kw))
                    
                except Exception as e:
                    #raise e
                    traceback.print_exc()

            logger.info('"%s" "%s"' % (addr[0],path) )
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
            req = 'HTTP/1.1 600 system error!\r\nContent-Length: %d\r\n\r\n%s' % (len(str(e)),str(e))
            #req = 'HTTP/1.1 500 system error!\r\n\r\n'
            new_sock.send(req.encode())
            new_sock.close()
        #service.__soketset.remove(clinet)
