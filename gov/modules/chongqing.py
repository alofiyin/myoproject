# -*- coding: utf-8 -*-
#Copyright  2015/4/21  fiyin
#重庆省模板


import pdb
import random
import json,time,re,os,random
from lxml import etree
import logging
import config 
from httpwrap import HttpWrap,http_upload_image
from threading import Thread
#from core import exec_main
import random
import datamodel
from urllib import request
import socket 

import traceback

"""模块化必须变量"""
#业务标识代码(以省份的简称命名，见datamodel.SF_DIST)
biz_flag = 'js'
#注册码解析服务器地址(可为空)
img_decode_url="http://192.168.10.126:1983/imgcode/cc_code" 
#记录被封的ip集合
ille_proxy_ip = set()
#计数
Ok_num   = 0
Null_num = 0
False_num = 0
#---------------#

logger = logging.getLogger('main.gov.%s'%biz_flag)

"""采集用到的url地址"""
#主页地址
url_home = 'http://gsxt.cqgs.gov.cn/'
#验证码地址
url_code = 'http://gsxt.cqgs.gov.cn/sc.action?width=130&height=50&fs=20&t=%s'
#验证码的验证地址
url_check= 'http://gsxt.cqgs.gov.cn/search.action'
#列表页地址
url_list= 'http://gsxt.cqgs.gov.cn/search_ent'
#信息提取地址
url_info = 'http://gsxt.cqgs.gov.cn/search_getEnt.action?entId=%s&id=%s&type=%s'
#----------------#

#用于匹配json结果
title_base={'entname':'name','regno':'reg_no','enttype':'type','estdate':'reg_date','注册日期':'reg_date','pril':'faren','lerep':'faren','name':'faren','法定代表人':'faren','regcap':'reg_capital','oploc':'addr','dom':'addr','住所':'addr','opscope':'biz_scope','opscoandform':'biz_scope','经营期限自':'open_date','opfrom':'open_date','opto':'close_date','经营期限至':'close_date','regorg':'reg_authority','issblicdate':'audit_date','opstate':'reg_status'}
		
def get_info(corp,proxyinfo=''):
	if len(corp) <4:
		return [corp,[],3,proxyinfo]
	socket.setdefaulttimeout(10)
	"""采集函数
	参数说明:
		corp  公司名称
		proxyinfo 代理ip  (格式为 ip:port) 为空时使用本机ip
	返回值说明:
	    status  状态码
	    base_info 采集到的工商信息
	"""
	#状态码 0 正常，1代理ip失效或者网站无法访问 2 ip被封 3公司不存在
	status = 0
	#基本信息
	base_info=[]
	#股东信息
	boss_info=[]
	#pdb.set_trace()
	#http模拟器
	http = HttpWrap()
	#设定代理ip格式 {"代理类型http|https":"ip:port"}
	if proxyinfo:
		http.set_proxy({'http':proxyinfo})
	res = http.request(url_home,method='GET')
	#访问主页面用于注册cookie信息,如果无法访问则直接返回失败
	if res.code != 200:
		#print(res.code)
		if res.code>200:
			ille_proxy_ip.add(proxyinfo)
		return [corp,base_info,1,proxyinfo]
	
	"""验证过程，循环验证直到成功"""
	#成功标识
	flag = 0	
	html=""
	cu_time = int(time.time())
	#出错次数
	err_type = 0 
	while flag ==0:
		if datamodel.g_exit:
			return [corp,base_info,1,proxyinfo]
		try:
			if err_type >10 :
				return [corp,base_info,1,proxyinfo]
			
			url = url_code % int(time.time())
			res = http.request(url,method='GET')
			data = {}
			#print('step...1')
			if res.code == 200:
	
				#保存验证码
				try:
					im = res.read()
				except:
					im=''
					time.sleep(1)
					continue

				code = http_upload_image(img_decode_url,im)

				#print(code)
				#手工输入验证码
				#code = raw_input('input the code:').decode('gbk').encode('utf-8')
				if not code:
					err_type+=1
					continue
				data={'key':corp,'code':code}
				#重新设置头
				http.reset_headers()
				http.set_header('Accetp','application/json, text/javascript, */*; q=0.08')
				http.set_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
				http.set_header('Referer',url_home)
				http.set_header('X-Requested-With','XMLHttpRequest')
				res = http.request(url_check,"POST",data)
				#print('step...3')
				if res.code == 200:
					html = http.read(res)
					if '验证码不正确' in html:
						continue
					if '您搜索的条件无查询结果' in html:
						return [corp,base_info,3,proxyinfo]

					break
				
				else:
					err_type+=1
					#print(res.code)
					time.sleep(5)
					#return [corp,base_info,1,proxyinfo]
			else:
				#print(res.code)
				if res.code == 403:
					time.sleep(20)
				err_type+=1
		
		except Exception as e:
			#traceback.print_exc()	
			err_type+=1
		time.sleep(1)
		if err_type>10:
			return [corp,base_info,1,proxyinfo]
	#提取数据		
	try:
		context = etree.HTML(html)
		nodes = context.xpath('//div[@class="item"]/a')
		#pdb.set_trace()
		for node in nodes:
			_base_info = {}
			entId, opid,entType = (node.get('data-entid'),node.get('data-id'),node.get('data-type'))
			name = node.text.strip()
			
			data = {'entId':entId,'id':opid,'type':entType,'name':name}
			page_res = http.request(url_list,'POST',data)
			page = http.read(page_res)
			page_txt = etree.HTML(page)
			data_type= re.findall('type=\'(\d+)\'',page_txt.get('ng-init'))[0]
			url = url_info % (entId,http.urlencode(opid),data_type)
			_base_info = format_html(url)
			if _base_info:
				base_info.append(_base_info)
		if base_info:
			return [corp,base_info,status,proxyinfo]
	except:
		#traceback.print_exc()
		return [corp,base_info,1,proxyinfo]	
	return [corp,base_info,status,proxyinfo]

def format_html(url):
	"""内容提取
	"""
	#pdb.set_trace()	
	result = {}
	data = {}
	boss = []
	
	http = HttpWrap()
	res = http.request(url)
	if res.code !=200:
		return False
	html = http.read(res,'b')
	try:
		item = json.loads(html[6:].decode())
		base = item['base']
		if 'investors' in item and item['investors']:
			for row in item['investors']:
				if 'inv' in row: 
					boss.append(row['inv'])
		if boss:
			result['shareholders']=json.dumps(boss)
		#注册资本
		if 'regcap' in base:
			if 'regcapcur' in base:
				base['regcap']="%s万%s" % (base['regcap'],base['regcapcur'])
			else:
				base['regcap']="%s万人民币" % base['regcap']
		for k,v in base.items():
			if k in title_base and v:
				result[title_base[k]] = v.strip()
			#else:
			#	print(k,v)
		result['gov_url'] = url
	except:
		traceback.print_exc()
		return False
	return result	

def input_info(res):
	print ("******%s*****"	% res[0])
	print ("基本信息")
	if type(res[1]) != list:
		res[1]=[res[1]]
	for itm in res[1]:
		for k,v in itm.items():
			print (k,v)
			#print "%s:	%s" % (k,v)
		print("-----------------")



				
if __name__ == "__main__":
	
	img_decode_url="http://127.0.0.1:1983/imgcode/cc_code"

	#res = get_info('常熟市国宇纺织有限公司')
	proxyinfo = {'http':'117.177.243.50:8080'}
	
	res = get_info('镇江舒格美鞋业有限公司',proxyinfo="")
	input_info(res)
	
