# -*- coding: utf-8 -*-
#Copyright  2015/4/21  fiyin
#江苏省模板


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
from eventlet.green.urllib import request
from eventlet.green import socket 
import eventlet
import traceback

"""模块化必须变量"""
#业务标识代码(以省份的简称命名，见datamodel.SF_DIST)
biz_flag = 'js'
#注册码解析服务器地址(可为空)
img_decode_url="http://127.0.0.1:1983/imgcode/base" 
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
url_home = 'http://www.jsgsj.gov.cn:58888/province/'
#验证码地址
url_code = 'http://www.jsgsj.gov.cn:58888/province/rand_img.jsp?type=8&temp=%s'
#验证码的验证地址
url_check= 'http://www.jsgsj.gov.cn:58888/province/infoQueryServlet.json?query_info=true'
#信息提取地址
url_info = 'http://qyxy.baic.gov.cn/gjjbj/gjjQueryCreditAction!getBjQyList.dhtml'
#----------------#

def get_info(corp,proxyinfo=''):
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
	base_info={}
	#股东信息
	boss_info=[]
    #用于匹配json结果
	title_base={'C2':'name','C1':'reg_no','C3':'type','C4':'reg_date','C5':'faren','C6':'reg_capital','C7':'addr','C8':'biz_scope','C9':'open_date','C10':'close_date','C11':'reg_authority','C12':'audit_date','C13':'reg_status'}

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
		#if datamodel.g_exit:
		#	return [corp,base_info,1,proxyinfo]
		try:
			rand_time = time.strftime('%a %b %d %Y %H:%M:%S GMT 0800')
			url = url_code #% rand_time
			res = http.request(url,method='GET')
			data = {}
			#print('step...1')
			if res.code == 200:
	
				#保存验证码
				try:
					im = res.read()
				except:
					im=''
					continue
				code = http_upload_image(img_decode_url,im)
					
				#手工输入验证码
				#code = raw_input('input the code:').decode('gbk').encode('utf-8')
				#print(code)
				#print('step...2')
				data={'name':corp,'verifyCode':code}
				#重新设置头
				http.reset_headers()
				http.set_header('Accetp','application/json, text/javascript, */*; q=0.01')
				http.set_header('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
				http.set_header('Referer',url_home)
				http.set_header('X-Requested-With','XMLHttpRequest')
				res = http.request(url_check,"POST",data)
				#print('step...3')
				if res.code == 200:
					html = http.read(res)
					jdata = json.loads(html)
					#print(jdata)
					if jdata[0]['TIPS'] and 'IP'  in jdata[0]['TIPS']:
						#print(jdata)
						ille_proxy_ip.add(proxyinfo)
						return [corp,base_info,2,proxyinfo]
					if "没有符合查询条件的结果" in jdata[0]['COUNT']:
						return [corp,base_info,3,proxyinfo]
					#	logger.info("iperror:%" % jdata[0]['TIPS'])
					#print ("res:",html)
					if not jdata[0]['TIPS']:
						html = jdata[0]['INFO']
						break
				else:
					err_type+=1
					#return [corp,base_info,1,proxyinfo]
			else:
				err_type+=1
			if err_type >10 :
				return [corp,base_info,1,proxyinfo]		
		except Exception as e:
			traceback.print_exc()	
		time.sleep(1)
	#pdb.set_trace()
	#列表页

	#取出详情页的url
	if not html:
		return [corp,base_info,1,proxyinfo]
	#print ("html:",html)
	try:
		
		context = etree.HTML(html)
		nodes = context.xpath("//a")
		link_info = nodes[0].attrib['onclick'].strip()[12:-2].replace("'",'').split(',')
		url ='http://www.jsgsj.gov.cn:58888%s' % (link_info[0].strip())
		data = {'containContextPath':link_info[5].strip(),'id':link_info[2].strip(),
			'name':'','org':link_info[1].strip(),'reg_no':link_info[4].strip(),'seq_id':link_info[3].strip()}
					
		#详情页基本资料
		#self.reset_headers()
		#self.set_headers('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
		#self.set_headers('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
		#self.set_headers('Referer','http://www.jsgsj.gov.cn:58888/province/queryResultList.jsp')
		#res = self.request(url)
		###############
		#http.reset_headers()
		'''
		self.set_headers('Accept','application/json, text/javascript, */*; q=0.01')
		self.set_headers('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
		self.set_headers('X-Requested-With','XMLHttpRequest')
		self.set_headers('Referer',http://www.jsgsj.gov.cn:58888/ecipplatform/inner_pspc/pspc_queryCorpInfor_gsRelease.jsp')
		'''
		http.headers={'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)','Accept-Encoding': 'gzip, deflate','Accept-Language': 'zh-CN'}
		http.headers['Accept']='application/json, text/javascript, */*; q=0.01'
		http.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
		http.headers['Referer'] = 'http://www.jsgsj.gov.cn:58888/ecipplatform/inner_pspc/pspc_queryCorpInfor_gsRelease.jsp'
		#基本资料
		url = "http://www.jsgsj.gov.cn:58888/ecipplatform/ciServlet.json?ciEnter=true"
		data={'id':link_info[2].strip(),'org':link_info[1].strip(),'seq_id':link_info[3].strip(),'specificQuery':'basicInfo'}
		base_info['gov_url']=json.dumps(data)
		res = http.request(url,'POST',data)
		#连接出错，做失败处理
		if  res.code==-1:
			print(res.code)
			return [corp,base_info,1,proxyinfo]
		info = res.read().decode()
		#print(res.code,info)
		data = json.loads(info)[0]
		base_info['corp_id']=link_info[2].strip()
		base_info['corp_org']=link_info[1].strip()
		base_info['corp_seq_id']=link_info[3].strip()
		for k,v in data.items():
			if k in title_base:
				base_info[title_base[k]]=v
				#股东信息
		url = 'http://www.jsgsj.gov.cn:58888/ecipplatform/ciServlet.json?ciEnter=true'
		data = {'CORP_ID':link_info[2].strip(),'CORP_ORG':link_info[1].strip(),'CORP_SEQ_ID':link_info[3].strip(),'pageNo':1,'pageSize':5,'showRecordLine':1,'specificQuery':'investmentInfor'}	

		res = http.request(url,'POST',data)
		#取股东出错，放弃股东信息，返回结果
		if res.code !=200:
			return [corp,base_info,status,proxyinfo]
		info = res.read().decode()
		#print(res.code,info)
		try:
			data = json.loads(info)
			for row in data['items']:
				boss_info.append([row['C1'],row['C2']])
			if boss_info:
				base_info['shareholders']=json.dumps(boss_info)
		except Exception as e:
			traceback.print_exc()
	except Exception as e:
		#traceback.print_exc()
		try:
			base_info['name']=corp
			base_info['reg_status']='已注销'
			pe={'reg_no':'注册号:\<span\>(.*?)\<',
				'faren':'法定代表人:\<span\>(.*?)\<|投资人:\<span\>(.*?)\<|经营者:\<span\>(.*?)\<',
				'reg_authority':'登记机关:\<span\>(.*?)\<',
				'cancell_date':'注销日期:\<span\>(.*?)\<|吊销日期:\<span\>(.*?)\<'}
			for k,v in pe.items(): 
				rs = re.findall(v,html)
				if rs:
					base_info[k] = rs[0]
					if type(rs[0]) in [list,tuple]:
						if rs[0][0]:
							base_info[k] = rs[0][0]
						elif rs[0][1]:
							base_info[k] = rs[0][1]
						elif(len(rs[0])>2):
							base_info[k] = rs[0][2]
		except:
			pass
		if 'reg_no' not in base_info:
			return [corp,base_info,1,proxyinfo]
	return [corp,base_info,status,proxyinfo]

def input_info(res):
	print ("******%s*****"	% res[0])
	print ("基本信息")
	for k,v in res[1].items():
		print (k,v)
		#print "%s:	%s" % (k,v)
	print("-----------------")



				
if __name__ == "__main__":
	
	#img_decode_url="http://127.0.0.1:1983/imgcode/base"

	#res = get_info('常熟市国宇纺织有限公司')
	#proxyinfo = {'http':'117.177.243.50:8080'}
	
	#res = get_info('常熟市兴达机械有限公司',proxyinfo="")
	#input_info(res)
	data={'seq_id': '6', 'specificQuery': 'basicInfo', 'org': '1402', 'id': '1597861'}
	http = HttpWrap()
	url = "http://www.jsgsj.gov.cn:58888/ecipplatform/ciServlet.json?ciEnter=true"
	res = http.request(url,'POST',data)
	print(res.read())
	
