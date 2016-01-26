# -*- coding: utf-8 -*-
#Copyright  2015/4/21  fiyin
#天津省模板


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
img_decode_url="http://192.168.10.126:1983/imgcode/tj_code" 
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
url_home = 'http://tjcredit.gov.cn/platform/saic/search.ftl'
#验证码地址
url_code = 'http://tjcredit.gov.cn/verifycode?date=%s'
#验证码的验证地址
url_check= 'http://tjcredit.gov.cn/platform/saic/search.ftl'
#列表页地址
#信息提取地址
url_info = 'http://tjcredit.gov.cn/platform/saic/viewBase.ft'
#----------------#

#用于匹配json结果
title_base={'名称':'name','注册号':'reg_no','注册号/统一社会信用代码':'reg_no','类型':'type','组成形式':'orgtype','成立日期':'reg_date','注册日期':'reg_date','负责人':'faren','经营者':'faren','投资人':'faren','法定代表人':'faren','注册资本':'reg_capital','经营场所':'addr','营业场所':'addr','住所':'addr','经营范围':'biz_scope','经营期限自':'open_date','营业期限自':'open_date','营业期限至':'close_date','经营期限至':'close_date','登记机关':'reg_authority','核准日期':'audit_date','登记状态':'reg_status'}

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

				#手工输入验证码
				#code = raw_input('input the code:').decode('gbk').encode('utf-8')
				if not code:
					err_type+=1
					continue
				data={'searchContent':corp,'vcode':code}
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
					#pdb.set_trace()
					if '您查询的信息多于' not in html:
						continue
					if '您查询的信息多于 0 条记录' in html:
						return [corp,base_info,3,proxyinfo]
					flag=1
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

	try:
		context = etree.HTML(html)
		nodes = context.xpath('//div[@class="content"]//a')
		#pdb.set_trace()
		for node in nodes:
			 
			#url = "http://tjcredit.gov.cn%s" % node.get('href')	
			entid = node.get('href').split('=')[1]
			url="http://tjcredit.gov.cn/platform/saic/baseInfo.json?entId=%s&departmentId=scjgw&infoClassId=dj" % entid	

			'''
			res = result.read().decode()
			jurl_result =re.findall('"/platform/saic/topInfoClass.json.*"',res)
			if not jurl_result:
				continue
			jurl = "http://tjcredit.gov.cn%s" % jurl_result[0][1:-1]
			j_result = http.request(jurl)
			if j_result.code !=200:
				continue
			jdata = json.loads(j_result.read().decode())
			base_url = "http://tjcredit.gov.cn%s" % jdata[0]['url']
			result = http.request(base_url)
			
			if result.code !=200:
				continue
			'''
			_base_info = format_html(url)
			if _base_info:
				base_info.append(_base_info)
			#else:
			#	print(html)
	except:
		traceback.print_exc()
		print(url)
		return [corp,base_info,1,proxyinfo]	
	
	return [corp,base_info,status,proxyinfo]

def format_html(url):
	"""内容提取
	"""
	#pdb.set_trace()	
	result = {}
	data = {}
	boss_info=[]
	keys_list = []
	value_list = []
	
	http = HttpWrap()
	res = http.request(url)
	if res.code !=200:
		return False
	html = http.read(res)
	try:
		context = etree.HTML(html) 
	except:
		return False
	nodes = context.xpath('//table[@class="result-table"][1]//tr')
	for node in nodes:
		item=node.getchildren()
		if not(item) or len(item)%2>0:
			continue
		for i in range(len(item)):
			txt = item[i].text
			if not txt:
				txt=""
			if (i+1)%2==0:
				value_list.append(txt.strip())
			else:
				keys_list.append(txt.strip())
												
	data = dict(map(lambda x,y:[x,y], keys_list,value_list))
	for k,v in data.items():
		if not k :
			continue
		if k in title_base and v:
			result[title_base[k]] = v.strip()
		else:
			print("K:",k,"V:",v)
	result['gov_url']=url
	#股东信息
	info = context.xpath('//table[@id="touziren"]//tr')
	try:
		if len(info) >2:
			info = info[2:]
		for node in info:
			boss_info.append([node.getchildren()[0].text.strip(),node.getchildren()[1].text.strip()])
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
	
	img_decode_url="http://192.168.10.126:1983/imgcode/tj_code"

	#res = get_info('常熟市国宇纺织有限公司')
	proxyinfo = {'http':'117.177.243.50:8080'}
	
	res = get_info('北京谊光物业管理有限公司天津分公司',proxyinfo="")
	input_info(res)
	
