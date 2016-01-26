#_*_coding:utf-8_*_

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved

#$Id: HttpWrap.py 649 2015-06-01 fiyin $#
__author__ = 'fiyin <alofiyin@gmail.com>'
__version__ = '$Revision: 0.1 $'

try:
    import urllib2
    from urllib import urlencode
    from cookielib import CookieJar
except:
    from urllib import request as urllib2
    from urllib.parse import urlencode
    from http.cookiejar import  CookieJar
from urllib.error import URLError, HTTPError
import socket ,random
import json,time,re
import hashlib
import gzip
import traceback
class HttpWrap_Except:
    code = -1
    reason = "sys error." 

class HttpWrap():
    __headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)','Accept': 'text/html, application/xhtml+xml, */*','Accept-Encoding': 'gzip, deflate','Accept-Language': 'zh-CN'}
    def __init__(self):
        self.operate = ''  # response的对象（不含read）
        self.cj = CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        #urllib2.install_opener(self.opener)
        self.headers = HttpWrap.__headers      
        self.data = {}  
    
    def set_proxy(self,info):
        proxy_handler = urllib2.ProxyHandler(info)
        self.opener = urllib2.build_opener(proxy_handler,urllib2.HTTPCookieProcessor(self.cj))
    
    def request(self,url,method='GET',data=None,debug=False):

        if data and method=='POST':
            if type(data) == dict:
                data = urlencode(data).encode()
            elif type(data)== str:
                data = data.encode()
        req = urllib2.Request(url,data,headers = self.headers)
        if method=='GET':       
            req.get_method = lambda: 'GET'
        try:
            result = self.opener.open(req)
            if debug:
                print("data:%s"%data)
                print("code:%s"%result.code)
                print("headers:%s"%str(self.headers))
        except HTTPError as e:
            return e
        except URLError as e:
            if hasattr(e, 'code'): 
                return e
            else:
                return HttpWrap_Except()
        except:
            return HttpWrap_Except()
        return result
    
    def urlencode(self,str):
        
        return urllib2.quote(str)
    
    def set_header(self,key,value):
        self.headers[key] = value
        
    def set_headers(self,item):
        assert(type(item) == dict) 
        self.headers = item
           
    def reset_headers(self):
        self.headers = HttpWrap.__headers
        
    def set_data(self,key,value):  
        self.data[key] = value  
           
    def set_data_item(self,item):  
        assert(type(item) == dict)      
        self.data = data
        
    def read(self,reason,format='s'):
        """取结果，如果使用了gzip则解压"""
        res = b''
        try:
            res = reason.read()
            if 'Content-Encoding' in reason.headers and reason.headers['Content-Encoding']=='gzip':
                res = gzip.decompress(res)

        except socket.timeout as e:
            pass
        except Exception as e:
            #traceback.print_exc()
            pass
        if format == 's':
        	return res.decode()
        return res
    
def http_upload_image( url,filebytes, paramDict={} ):
    """
    上传文件 比如图片
    参数说明:
    url           提交的目标地址
    filebytes     文件二进制流
    paramDict     其它的字段
    """    
    try:
        http = HttpWrap() 
        timestr = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        boundary = '------------' + hashlib.md5(timestr.encode()).hexdigest().lower()
        boundarystr = '\r\n--%s\r\n'%(boundary)
        
        bs = b''
        for key,value in paramDict.items():
            bs = bs + boundarystr.encode()
            param = "Content-Disposition: form-data; name=\"%s\"\r\n\r\n%s"%(key, value)
            #print param
            bs = bs + param.encode()
        bs = bs + boundarystr.encode()
            
        header = 'Content-Disposition: form-data; name=\"image\"; filename=\"%s\"\r\nContent-Type: image/gif\r\n\r\n'%('sample')
        bs = bs + header.encode()
        
        bs = bs + filebytes
        tailer = '\r\n--%s--\r\n'%(boundary)
        bs = bs + tailer.encode()
        
        headers = {'Content-Type':'multipart/form-data; boundary=%s'%boundary,
                   'Connection':'Keep-Alive',
                   'Expect':'100-continue',
                   }
        http.set_headers(headers)
        #response = requests.post(url, params='', data=bs, headers=headers)
        response=http.request(url,'POST',bs)

        if response.code ==200:
            return response.read().decode()
        else:
            return ""
    except:
        traceback.print_exc()
        return ""