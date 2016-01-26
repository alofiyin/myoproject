# -*- coding: utf-8 -*-
#$Id: SrvEventlet.py 3316 2015-08-02 10:27:53Z fyin $
# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
#工商二维码解析

from PIL import Image, ImageEnhance,ImageFilter
from zbar import Zbar
from io import BytesIO
import time,pdb
from urllib.parse import urlparse
#from httpwrap import HttpWrap
from urllib import request
import json

GovP={'www.gzonline.gov.cn':'http://www.gzonline.gov.cn/cri/BusinessInfoMobile/Content_JCXX.aspx?zch=%s'}
def info(kw):
	#解析二维码内容
	#print(kw.split(b'\r\n\r\n'))
	try:
		im = Image.open(BytesIO(kw['body']))
	except Exception as e:
		#raise("illegal Image File!")
		return False
	#image2 = im.filter(ImageFilter.MedianFilter())
	#enhancer = ImageEnhance.Contrast(image2)
	#im = enhancer.enhance(2)
	#im = im.convert('1')
	z = Zbar(im, scratch_image_name='/tmp/%s.bmp'%time.time())
	text = z.image_to_string()
	return text
	
def govinfo(kw):
	text = info(kw)
	res={}
	if text:
		s = text[8:]
		for row in s.split('|'):
			itm = row.split('：')
			res[itm[0]]=itm[1]			
	return res

def check(kw):
	data = govinfo(kw)
	#print(data)
	url = data['数据查询链接']
	parse = urlparse(url)
	host = parse.netloc
	query = parse.query
	id = query[query.index('=')+1:]
	res =request.urlopen(GovP[host] % id).read()
	
	print(res.decode())
	

	