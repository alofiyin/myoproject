#_*_coding:utf-8_*_

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#工头服务程序
#$Id: contractio_servic.py 649 2015-06-12 fiyin $#

from eventlet_srvd import ENTService
import logging
import pdb,time
import traceback
import tasks 
import task_reg_model
from httpparse import HttpParse
from imp import reload
import commands_
from rediswrap import json_dumps, json_loads
import cronthread

logger = logging.getLogger('main')
def reload_tasks():
    reload(tasks)

def reload_cmd():
    reload(commands_)
        

class WEBServic(ENTService):
    def __init__(self):
        super(WEBServic, self).__init__()
    
              
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
                if html._Header['Method']=='POST':
                    print(html._Header)
                    body_len = int(html._Header['content-length'])
                    if len(html._DATA) < body_len:
                        while 1:
                            c = new_sock.recv(512)
                            html._DATA = html._DATA + c
                            if len(html._DATA) >= body_len:
                                break
                        if html._Header['Content-Type'].index('multipart/form-data') >-1:
                            html._parse_multipart()
                        else:
                            html._parse_post()
            except Exception as e:
                raise Exception('The request of the error')
            path = html._Header['Request']
            #action, func = path.split('/')[:2]
            query = html.getpath()
            action, func = query[:2]
            
            args = ()
            if action == 'cmd': 
                kw  = html._GET or html._POST or json_loads(html._DATA) or {}

                if func == 'reload_tasks':
                    reload_tasks()
                    rs = "OK"
                elif func == 'reload_cmd':
                    reload_cmd()
                    rs = "OK"
                else:
                    models = dir(commands_)
                    if func in models:
                        f = eval('commands_.%s' % func)
                        rs = json_dumps(f(*args,**kw))
                logger.info('"%s" "%s" "cmd"' % (addr[0],path) )
            elif action =='api':
                try:
                    exec("from api.%s import %s" % (query[1],query[2]))
                    f = eval(func)
                    rs = json.dumps(f(kw))
                except Exception as e:
                    rs = str(e)    
            elif action == 'cron':
                if func == 'add':
                    kw  = json_loads(html._DATA)
                    cron={}
                    cron['func'] = kw.pop('func')
                    cron['cron_info'] = kw.pop('cron_info')
                
                    if 'biz' not in kw:
                        cron['biz'] = func
                    else:
                        cron['biz'] = kw['biz']
                        
                    cron['args'] = kw
                    cronthread.add_cron(cron)
                elif func == 'remove':
                    kw = html._GET
                    cronthread.remove_cron(kw['func'],kw['biz'])
                rs = '{"status":1}'
            else:             
                kw  = json_loads(html._DATA)
                #print(html._Header['Method'],html._DATA,html._POST)
                if 'biz' not in kw:
                    kw['biz'] = func
                taskid = "%s-%s-%s" % (func,time.strftime('%Y%m%d'),int(time.time()))
                kw['pid'] = taskid
                kw['func'] = func
                
                kw['job_type'] = task_reg_model.task_list[func]['type']
                rs = task_reg_model.task_registry[func](*args,**kw)
                
                logger.info('"%s" "%s" "task" "%s"' % (addr[0],path,taskid))
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
            logger.error('"%s" "%s" "erron" "%s"' % (addr[0],path,errinfo))
            req = 'HTTP/1.1 500 system error!\r\nContent-Length: %d\r\n\r\n%s' % (len(str(e)),str(e))
            #req = 'HTTP/1.1 500 system error!\r\n\r\n'
            new_sock.send(req.encode())
            new_sock.close()
        #service.__soketset.remove(clinet)
