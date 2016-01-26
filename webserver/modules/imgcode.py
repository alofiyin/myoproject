#_*_coding:utf-8_*_
#$Id: SrvEventlet.py 3316 2015-08-02 10:27:53Z fyin $
# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
#验证码识别 需要 

from PIL import Image,ImageEnhance,ImageFilter
import pytesser
from io import BytesIO
from httpwrap import http_upload_image
import time,json,re
import traceback

#ocr识别
def get_txt(im,lang='eng'):
	image_name = '/tmp/'+str(time.time())+'.bmp'
	text_name_root = '/tmp/'+str(time.time())
	pt = pytesser.pytesser(im,lang,scratch_image_name=image_name,scratch_text_name_root=text_name_root,tesseract_exe_name='tesseract')
	return pt.image_to_string().strip()	

#基本识别
def base(kw):
	try:
		image = Image.open(BytesIO(kw['body']))
	except Exception as e:
		#raise("illegal Image File!")
		print(e)
		return False
	#image = Image.open(imstr)
	#box = (0,18,142,41)
	#image = image.crop(box)
	image2 = image.filter(ImageFilter.MedianFilter())#中值过滤可以去掉大部分噪点
	enhancer = ImageEnhance.Contrast(image2)
	im = enhancer.enhance(2)
	im = im.convert('1')
	#im.save('test/' + str(time.time())+'.jpg','jpeg')
	return get_txt(im).replace(' ','')	

def ysdm(kw):
	"""云速打码
	http://ysdm.net/
	"""
	url="http://api.ysdm.net/create.json"
	try:
		image = Image.open(BytesIO(kw['body']))
		
	except Exception as e:
		#raise("illegal Image File!")
		print(e)
		return False
	paramDict={'username':'alofiyin',
				'password':'z123x654',
				'typeid':5000,
				'timeout':90,
				'softid':1,
				'softkey':'b40ffbee5c1cf4e38028c197eb2fc751'}
	res = http_upload_image(url,kw['body'], paramDict)
	try:
		rs = json.loads(res)
		return rs['Result']
	except:
		return ''

def zh_simple(kw):
	try:
		image = Image.open(BytesIO(kw['body']))
	except Exception as e:
		#raise("illegal Image File!")
		#print(e)
		return False
	#image = Image.open(imstr)
	#box = (0,18,142,41)
	#image = image.crop(box)
	enhancer=ImageEnhance.Color(image)
	im = enhancer.enhance(15)
	im = im.convert('L')
	#im.save('test/' + str(time.time())+'.jpg','jpeg')
	return get_txt(im,lang='chi_sim').replace(' ','')	
	
def pointmidu(im):
	"""去色只保留黑色"""
	w,h = im.size
	#import pdb
	#pdb.set_trace()
	box = (0,0,int(w/2),h)
	im1=im.crop(box)
	data = list( im1.getdata() )

	w,h = im1.size
	for x in range(w):
		for y in range(h):
			p = data[ y*w + x ]
			if sum(p)>100:
				im1.putpixel((x,y), 16777215)#填充白色
	return im1			

def pointmidu2(im):
	"""去色只保留红色"""
	w,h = im.size
	box = (0,0,int(w/2),h)
	im1=im.crop(box)
	data = list( im1.getdata() )
	w,h = im1.size
	for x in range(w):
		for y in range(h):
			p = data[ y*w + x ]
			#print(p)
			if p[0]>100 and p[1]<100 and p[2]<100:
				pass
			else:
				im1.putpixel((x,y), 16777215)
	return im1
def cc_code(kw):
	"""
	重庆专用
	http://gsxt.cqgs.gov.cn/sc.action?width=130&height=50&fs=20
	"""
	s=0
	try:
		image = Image.open(BytesIO(kw['body']))
	except Exception as e:
		#raise("illegal Image File!")
		traceback.print_exc()
		return False
	im=pointmidu(image)
	res = get_txt(im,lang='chi_sim').replace(' ','')	
	numbs = re.findall(r'\d',res)
	if len(numbs) >1:
		if '加' in res or '力口' in res or '刀口' in res:
			s=int(numbs[0])+int(numbs[1])
		else:
			s = int(numbs[0])-int(numbs[1])
	return s
def tj_code(kw):
	"""
	天津专用
	http://tjcredit.gov.cn/verifycode?date=1430129817469
	"""
	s=0
	try:
		image = Image.open(BytesIO(kw['body']))
	except Exception as e:
		#raise("illegal Image File!")
		traceback.print_exc()
		return False
	im=pointmidu2(image)
	res = get_txt(im,lang='chi_sim').replace(' ','')	
	numbs = re.findall(r'\d',res)
	if len(numbs) >1:
		if '加' in res or '力口' in res or '刀口' in res:
			s=int(numbs[0])+int(numbs[1])
		elif '乘' in res:
			s=int(numbs[0])*int(numbs[1])
		elif '除' in res:
			s=int(numbs[0])/int(numbs[1])
		else:
			s = int(numbs[0])-int(numbs[1])
	return s	
	
if __name__=="__main__":
	import urllib
	kw={}
	kw['body'] = open('test.jpg','rb').read()
	kw['body'] = urllib.request.urlopen('http://tjcredit.gov.cn/verifycode?date=52165454545').read()
	res=tj_code(kw)
	print(res)
