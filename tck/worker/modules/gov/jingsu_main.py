# -*- coding: utf-8 -*-
#Copyright  2015/4/21  fiyin
#江苏省

from cls import *
import pdb
import urllib,urllib2,cookielib,socket ,random
import json,time,re,os
from imgcode import img2code_jiangsu
from lxml import etree
import linecache
import logging
import Queue

from threading import Thread

LOG_FILENAME = 'logs/jiansu_sys.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)


class gov_gd(webrobot):
	def __init__(self):
		webrobot.__init__(self)
		self.url_home = 'http://www.jsgsj.gov.cn:58888/province/'
		self.url_code = 'http://www.jsgsj.gov.cn:58888/province/rand_img.jsp?type=8&temp=%s'
		self.url_check= 'http://www.jsgsj.gov.cn:58888/province/infoQueryServlet.json?query_info=true'
		self.url_info = 'http://qyxy.baic.gov.cn/gjjbj/gjjQueryCreditAction!getBjQyList.dhtml'
		self.img_file_name = 'bj.png'
	def get_cookie(self):
		self.reset_headers()
		res = self.request(self.url_code,method='GET')
		return res.code
	def get_info(self,corp):
		#定义字段
		base_info={}
		boss_info=[]
		change_info={}
		title_base={'C2':'name','C1':'reg_no','C3':'type','C4':'reg_date','C5':'faren','C6':'reg_capital','C7':'addr','C8':'biz_scope','C9':'open_date','C10':'close_date','C11':'reg_authority','C12':'audit_date','C13':'reg_status'}

		#pdb.set_trace()
		self.get_cookie()
		flag = 0
		#验证码
		cu_time = int(time.time())
		while flag ==0:
			rand_time = time.strftime('%a %b %d %Y %H:%M:%S GMT 0800')
			url = self.url_code #% rand_time
			res = self.request(url,method='GET')
			data = {}
			if res.code == 200:
				#保存验证码
				try:
					code = img2code_jiangsu(res.read())
				except:
					continue
				#手工输入验证码
				#code = raw_input('input the code:').decode('gbk').encode('utf-8')
				print code
				self.set_data({'name':corp,'verifyCode':code})
				#重新设置头
				self.reset_headers()
				self.set_headers('Accetp','application/json, text/javascript, */*; q=0.01')
				self.set_headers('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
				self.set_headers('Referer',self.url_home)
				self.set_headers('X-Requested-With','XMLHttpRequest')
				res = self.request(self.url_check)
				if res.code == 200:
					html = res.read()
					jdata = json.loads(html)
					print "res:",html.decode('utf-8')
					if not jdata[0]['TIPS']:
						html = jdata[0]['INFO']
						break
					
			time.sleep(1)
		#pdb.set_trace()
		#列表页

		#取出详情页的url
		if not html:
			return False
		print "html:",html
		try:
			
			context = etree.HTML(html)
			nodes = context.xpath("//a")
			link_info = nodes[0].attrib['onclick'].strip()[12:-2].replace("'",'').split(',')
			url ='http://www.jsgsj.gov.cn:58888%s' % (link_info[0].strip())
			self.data = {'containContextPath':link_info[5].strip(),'id':link_info[2].strip(),
				'name':'','org':link_info[1].strip(),'reg_no':link_info[4].strip(),'seq_id':link_info[3].strip()}
					
			#详情页基本资料
			#self.reset_headers()
			#self.set_headers('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
			#self.set_headers('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
			#self.set_headers('Referer','http://www.jsgsj.gov.cn:58888/province/queryResultList.jsp')
			#res = self.request(url)
			###############
			self.reset_headers()
			'''
			self.set_headers('Accept','application/json, text/javascript, */*; q=0.01')
			self.set_headers('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
			self.set_headers('X-Requested-With','XMLHttpRequest')
			self.set_headers('Referer','http://www.jsgsj.gov.cn:58888/ecipplatform/inner_pspc/pspc_queryCorpInfor_gsRelease.jsp')
			'''
			self.headers={'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)','Accept-Encoding': 'gzip, deflate','Accept-Language': 'zh-CN'}
			self.headers['Accept']='application/json, text/javascript, */*; q=0.01'
			self.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
			self.headers['Referer'] = 'http://www.jsgsj.gov.cn:58888/ecipplatform/inner_pspc/pspc_queryCorpInfor_gsRelease.jsp'
			#基本资料
			url = "http://www.jsgsj.gov.cn:58888/ecipplatform/ciServlet.json?ciEnter=true"
			self.data={'id':link_info[2].strip(),'org':link_info[1].strip(),'seq_id':link_info[3].strip(),'specificQuery':'basicInfo'}
			res = self.request(url)
			info = res.read()
			print res.code,info
			data = json.loads(info)[0]
			base_info['corp_id']=link_info[2].strip()
			base_info['corp_org']=link_info[1].strip()
			base_info['corp_seq_id']=link_info[3].strip()
			for k,v in data.items():
				if title_base.has_key(k):
					base_info[title_base[k]]=v
	
			#股东信息
			url = 'http://www.jsgsj.gov.cn:58888/ecipplatform/ciServlet.json?ciEnter=true'
			self.data = {'CORP_ID':link_info[2].strip(),'CORP_ORG':link_info[1].strip(),'CORP_SEQ_ID':link_info[3].strip(),'pageNo':1,'pageSize':5,'showRecordLine':1,'specificQuery':'investmentInfor'}	
			res = self.request(url)
			info = res.read()
			print res.code,info
			data = json.loads(info)
			for row in data['items']:
				boss_info.append([row['C1'],row['C2']])
		except:
			base_info['name']=corp.decode('utf-8')
			base_info['reg_status']='已注销'.decode('utf-8')
			pe={'reg_no':'注册号:\<span\>(.*?)\<',
			'faren':'法定代表人:\<span\>(.*?)\<|投资人:\<span\>(.*?)\<|经营者:\<span\>(.*?)\<',
			'reg_authority':'登记机关:\<span\>(.*?)\<',
			'cancell_date':'注销日期:\<span\>(.*?)\<|吊销日期:\<span\>(.*?)\<'}
			for k,v in pe.items(): 
				rs = re.findall(v.decode('utf-8'),html)
				if rs:
					base_info[k] = rs[0]
					if type(rs[0]) in [list,tuple]:
						if rs[0][0]:
							base_info[k] = rs[0][0]
						elif rs[0][1]:
							base_info[k] = rs[0][1]
						elif(len(rs[0])>2):
							base_info[k] = rs[0][2]
		return [corp,base_info,boss_info]

def input_info(res):
	print "******%s*****"	% res[0]
	print u"基本信息"
	for k,v in res[1].items():
		print k,v
		#print "%s:	%s" % (k,v)
	print "-----------------"
	print u"股东信息"
	for row in res[2]:
		print row[0],row[1]


class robmain(Thread):
	def __init__(self,Q,_index):
		super(robmain, self).__init__()
		
		self.accessfile = 'logs/jiangsu/access.log'
		self.errofile = 'logs/jiangsu/erron.log'
		self.acc_fp = open(self.accessfile,'ab')	
		self.err_fp = open(self.errofile,'ab')	
		self.Q = Q
		self._index = _index
		self.exit = 1
	def run(self):
		while self.exit:
			#print 'Thread:',self.Q.qsize()
			if self.Q.qsize() == 0:
				time.sleep(1)
				continue
			corp = self.Q.get(block=0)

			try:
				gs = gov_gd()
				res = gs.get_info(corp)
				if res:
					input_info(res)
					self.acc_fp.write('%s\n' % json.dumps(res))
					res,desc = savedata(res[1],'jiangsu')
					if res == -1:
						self.err_fp.write("%s\n" %desc)
					print "savedata:",res,desc
					
				else:
					self.err_fp.write("%s\n" %corp)
				self._index +=1
			except Exception,e:
				logging.info(corp)
				logging.error(str(e))
				print 'err:',e
	def stop(self):
		self.exit = 0
def main():
	datafile = 'data/101112.txt'
	indexfile = 'logs/jiangsu.index'
	_index = 1
	Q = Queue.Queue()
	count = len(linecache.getlines(datafile,'rb'))
	if os.path.exists(indexfile):
		s=open(indexfile,'r').read().strip()
		if s:
			_index = int(s)
		#index = int(open(indexfile,'r').read().strip()	)
	x = _index
	line = _index
	thr = []
	for i in range(0,1):
		thr.append(robmain(Q,_index))
		
		thr[i].setDaemon(True)
		thr[i].start()
	while 1:
		
		#write_file(indexfile,str(line))
		#print Q.qsize()
		if Q.qsize() >=10:
			time.sleep(2)
			continue
			
		#corp = linecache.getline(datafile,line).strip()
		corp = linecache.getline(datafile,line).split(',')[1]
		line +=1
		if corp:
			Q.put(corp)
		if _index > x:
			write_file(indexfile,str(_index))
			x = _index
		if line >= count:
			break
	for t in thr:
		t.stop()
				
if __name__ == "__main__":
	
	main ()
	'''
	gs = gov_gd()
	#res = gs.get_info('常熟市国宇纺织有限公司')
	res = gs.get_info('苏州市徐家桥瓷土厂')
	print "******%s*****"	% res[0]
	print u"基本信息"
	for k,v in res[1].items():
		print k,v
		#print "%s:	%s" % (k,v)
	print "-----------------"
	print u"股东信息"
	for row in res[2]:
		print ', '.join(row)		
	
	'''
