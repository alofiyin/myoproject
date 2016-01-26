#_*_coding:utf-8_*_
#$Id: SrvEventlet.py 3316 2015-06-02 10:27:53Z fyin $
# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
#Eventlet  操作类
# All rights reserved

import eventlet
import time
import threading


class ENTService:
    __ip = '0.0.0.0'
    __port = 1982
    __size = 1000
    def __init__(self,ip=__ip,port=__port,size=__size):
        self._ip = ip
        self._port = port
        self._size = size 
        #self._pool = eventlet.GreenPool(self._size)
        self._request = 0
        self._report = 0
        #self._pool.spawn_n(self.listen())
        
    def get(self,client,buffsize=1024):
        req = ""
        self._request += 1
        while True:
            c = client.recv(buffsize)
            if not len(c): break
            
            req= "%s%s" %(req,c)        
        return req        	        
                        
    def handle(self,client,address):
        req = self.get(client)
        req = 'HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s'%(len(req),req)
        client.sendall(req.encode())
        client.close()
        self._report += 1
        #service.__soketset.remove(clinet)

            
    def listen(self):
        server = eventlet.listen((self._ip, self._port))
        while True:
            client = server.accept()
            #self._pool.spawn_n(self.handle, client)
            threading.Thread(target=self.handle,(client))
if __name__ == '__main__':
    srv = ENTService()
    srv.listen()
    #srv._pool.spawn_n(srv.listen())
    '''
    t1 = threading.Thread(target=srv.listen)
    t1.setDaemon(True)
    t1.start()
    c = 0
    while True:
        print c,srv._request,srv._report,srv._report-c
        c = srv._request 
        time.sleep(1)
    '''
    #srv.listen()
    