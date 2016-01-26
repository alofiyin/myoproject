# -*- coding: utf-8 -*-
#Copyright  2015/4/21  fiyin
#安徽省模板


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
img_decode_url="http://192.168.10.126:1983/imgcode/zh_simple" 
#记录被封的ip集合
ille_proxy_ip = set()
#计数
Ok_num   = 0
Null_num = 0
False_num = 0
#---------------#

logger = logging.getLogger('main.gov.%s'%biz_flag)

"""采集用到的url地址"""
host = "http://www.ahcredit.gov.cn"
#主页地址
url_home = 'http://www.ahcredit.gov.cn/search.jspx'
#验证码地址
url_code = 'http://www.ahcredit.gov.cn/validateCode.jspx?type=1&id=%s'
#验证码的验证地址
url_check= 'http://www.ahcredit.gov.cn/checkCheckNo.jspx'
#列表页地址
url_list= 'http://www.ahcredit.gov.cn/searchList.jspx'
#信息提取地址
url_info = 'http://qyxy.baic.gov.cn/gjjbj/gjjQueryCreditAction!getBjQyList.dhtml'
#----------------#
#用于匹配json结果
title_base={'名称':'name','统一社会信用代码/注册号':'reg_no','注册号':'reg_no','类型':'type','成立日期':'reg_date','注册日期':'reg_date','负责人':'faren','经营者':'faren','投资人':'faren','执行事务合伙人':'faren','法定代表人':'faren','注册资本':'reg_capital','经营场所':'addr','主要经营场所':'addr','营业场所':'addr','住所':'addr','业务范围':'biz_scope','经营范围':'biz_scope','经营期限自':'open_date','营业期限自':'open_date','合伙期限至':'close_date','合伙期限自':'open_date','营业期限至':'close_date','经营期限至':'close_date','登记机关':'reg_authority','核准日期':'audit_date','登记状态':'reg_status','组成形式':'orgtype',}

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
			rand_time = time.strftime('%a %b %d %Y %H:%M:%S GMT 0800')
			url = url_code % time.time()
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
				
				try:
					code = json.loads(code)	
				except Exception as e:
					#traceback.print_exc()
					continue
					
				#print(code)
				#手工输入验证码
				#code = raw_input('input the code:').decode('gbk').encode('utf-8')
				if not code:
					err_type+=1
					continue
				data={'checkNo':request.quote(code)}
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
					#print(html)
					jdata = json.loads(html)
					#print(jdata)
					if jdata=='{success:true}':
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
			pass
		time.sleep(1)
	#pdb.set_trace()
	#列表页
	
	try:
		data = {'checkNo':code,'entName':corp}

		res = http.request(url_list,'POST',data)
		if  res.code==-1:
			#print('get html :',res.code)
			return [corp,base_info,1,proxyinfo]
		#pdb.set_trace()
		html = http.read(res)

		if '无查询结果' in html:
			#print('您搜索的条件无查询结果')
			return [corp,base_info,3,proxyinfo]

		try:
			context = etree.HTML(html)
		except:
			print(html)
			return [corp,base_info,1,proxyinfo]
		url_nodes = context.xpath('//div[@class="list"]//a')
		if not url_nodes:
			return [corp,base_info,1,proxyinfo]
		for url_node in url_nodes:
			try:
				url="%s%s" % (host,url_node.get("href"))
				_base_info = format_html(url)
				if _base_info:
					base_info.append(_base_info)
			except Exception as e:
				traceback.print_exc()	
				if 'reg_no' not in base_info:
					base_info.append(_base_info)
	except Exception as e:
		traceback.print_exc()
		return [corp,base_info,1,proxyinfo]
	return [corp,base_info,status,proxyinfo]

def format_html(url,proxyinfo=""):
	"""内容提取
	"""
	result = {}
	data = {}
	boss_info=[]
	keys_list = []
	value_list = []
	
	#pdb.set_trace()
	http = HttpWrap()
	if proxyinfo:
		http.set_proxy({'http':proxyinfo})
	res = http.request(url)
	if res.code !=200:
		return False
	html = http.read(res)
	try:
		context = etree.HTML(html) 
	except:
		return False
	nodes = context.xpath('//div[@id="jibenxinxi"]//tr')
	result['corp_seq_id']=url.split('=')[1]
	data={}
	keys_list=[]
	value_list=[]
	for node in nodes:
		item=node.getchildren()
		if not(item) or len(item)%2>0:
			continue
		for n in item:
			if n.tag=='th':
				keys_list.append(n.text)
			elif n.tag=='td':
				value_list.append(n.text)
	
	data = dict(map(lambda x,y:[x,y], keys_list,value_list))
	for k,v in data.items():
		if not k :
			continue
		if k in title_base and v:
			result[title_base[k]] = v.strip()
		#else:
		#	print( k,v)
	result['gov_url']=url
	#股东信息
	info = context.xpath('//div[@id="invDiv"]//tr')
	try:
		for node in info:
			boss_info.append(node.getchildren()[1].text.strip())
	except Exception as e:
		traceback.print_exc()
	if boss_info:
		result['shareholders']=json.dumps(boss_info)		

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
	
	img_decode_url="http://127.0.0.1:1983/imgcode/zh_simple"

	#res = get_info('常熟市国宇纺织有限公司')
	proxyinfo = {'http':'117.177.243.50:8080'}
	
	res = get_info('鞋业有限公司',proxyinfo="")
	input_info(res)
	
