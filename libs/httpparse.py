#_*_coding:utf-8_*_
#$Id: SrvEventlet.py 3316 2015-06-02 10:27:53Z fyin $
# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
#http协议解析类 python3版本
# All rights reserved
import re
from urllib.parse import unquote
from urllib.parse import urlparse
import json
import pdb
def urlencode(s):
    reprStr = repr(s).replace(r'\x', '%')
    return reprStr[1:-1]

class HttpParse:
    def __init__(self,body):
        self.body = body
        self._Header = {}
        self._GET = {}
        self._POST = {}
        self._DATA = b""
        self.Up_File = {}
        
        self._parse()
        #self._parse_post()
    def _parse(self):
        """
        解析http内容，输出http头和数据
        """ 
        try:
            sp_index = self.body.index(b'\r\n\r\n')
            
            item = self.body.split(b'\r\n\r\n')
            _head = self.body[:sp_index].decode()
            
            if len(self.body) > sp_index+5:
                self._DATA = self.body[sp_index+4:]
            header_list = _head.split('\r\n')
            _handle = header_list.pop(0)
            self._Header['Method'], self._Header['Request'], self._Header['Version'] = _handle.split(' ')
            for line in header_list:
                k,v = line.lower().split(': ',1)
                self._Header[k]=v

            url = unquote(self.urlparse().query)
            if url:
                for i in url.split('&'):
                    ii = i.split('=')
                    if len(ii)>1:
                        self._GET[ii[0]] = ii[1]
                    else:
                        self._GET[ii[0]] = ""
        except Exception as e:
            return(None,None)
    def GET(self,key):
        if key in self._GET:            
            return self_GET[key]
        else:
            return ""
            
    def _parse_post(self):
        if "content-type" in self._Header and 'json' in self._Header['content-type']:
            try:
                self._POST = json.loads(self._DATA.decode())
                return
            except:
                
                pass
        try:
            data = self._DATA.decode()
        except:
            return {'body':self._DATA}
        try:
            for i in self._data.split('&'):
                ii = i.split('=')
                if len(ii)>1:
                    self._POST[ii[0]] = ii[1]
                else:
                    self._POST[ii[0]] = ""
        except Exception as e:
            #print(e)  
            pass              
    def _parse_multipart(self):
        #pdb.set_trace()
        boundary = self._Header['content-type'][self._Header['content-type'].rindex('boundary=')+9:] + '\r\n'
        boundary = boundary.encode()
        data = self._DATA.split(b'--'+boundary)[-1]
        start_px = data.index(b'\r\n\r\n')
        end_ps = len(boundary)+6
        head = data[:start_px]
        filebey = data[start_px+4:-end_ps]
        self.Up_File={'head':head,'body':filebey}

    def POST(self,key):
        if key in self._GET:            
            return self_GET[key]
        else:
            return ""   
                   
    def REQUES(self,key):
        return self.GET(key) or self.POST(key)   
    
    def urlparse(self):
        return urlparse(self._Header['Request'])
        
    def getpath(self):
        p = self.urlparse().path.split('/')
        while '' in p:
            p.remove('')
        return p
        