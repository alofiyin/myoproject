# -*- coding: utf-8 -*-
#Copyright  2015/8/21  fiyin
import mysqlwrap
import rediswrap
import time,json
from threading import Thread
from httpwrap import HttpWrap
queue_threshold = 2000 #队列阀值
rows_limit      = 1000  #每次从数据库获取记录数
g_exit			= False #全局退出标识
proc_title      = 'gov-service' #程序名

def get_baseindex_hash():
	"""数据源(存放待验证的公司名称以base_为前缀的mysql表)已提取的索引表，记录最后提取的记录id号
	数据格式：
	{
	  'mysql数据表名':最后提取的id号
	}
	"""
	name = "wbsp:gov:baseindex"
	return rediswrap.get_hash(name)
	
def get_row_queue(tbname):
	"""存放待验证的公司名称的队列
	   @name 以base_为前缀的mysql表
	"""
	name = "wbsp:gov:queue.base_" + tbname
	return rediswrap.get_queue(name)

def get_tmp_queue():
	"""
	存放插入数据库失败的记录
	"""
	name = "wbsp:gov:queue.tmp"
	return rediswrap.get_queue(name)	
		
def get_proxy():
	"""提取代理ip
	"""
	http = HttpWrap()
	proxyip=[]
	url = "http://192.168.10.126:1982/cmd/get_proxyip"
	res = http.request(url)
	if res.code==200:
		try:
			proxyip = json.loads(res.read().decode())		
		except:
			pass
	return proxyip
	

#公司源表结构	
Base_tb="""CREATE TABLE base_%s (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(50) COLLATE utf8_bin DEFAULT NULL,
  bizid int(11) DEFAULT NULL,
  flag int(11) DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY name (name)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
"""
#公司数据表结构
Data_tb="""CREATE TABLE data_%s (
  id int(11) NOT NULL AUTO_INCREMENT,
  name varchar(100) NOT NULL COMMENT '公司名称',
  reg_no varchar(50) DEFAULT NULL COMMENT '注册号',
  type char(20) DEFAULT NULL COMMENT '公司类型',
  faren varchar(20) DEFAULT NULL COMMENT '法定代表人',
  reg_capital varchar(50) DEFAULT NULL COMMENT '注册资本',
  reg_date varchar(20) DEFAULT NULL COMMENT '成立时间',
  addr varchar(50) DEFAULT NULL COMMENT '住所',
  open_date varchar(20) DEFAULT NULL COMMENT '营业期限自',
  close_date varchar(20) DEFAULT NULL COMMENT '营业期限至',
  biz_scope varchar(500) DEFAULT NULL COMMENT '经营范围',
  reg_authority varchar(50) DEFAULT NULL COMMENT '登记机关',
  audit_date varchar(20) DEFAULT NULL COMMENT '核准日期',
  reg_status varchar(10) DEFAULT NULL COMMENT '登记状态',
  corp_id int(11) DEFAULT NULL COMMENT '在公司网站的编号',
  corp_org int(11) DEFAULT NULL COMMENT '在工商网站的分组号',
  corp_seq_id varchar(50) DEFAULT NULL COMMENT '在工商网的参数',
  cancell_date varchar(20) DEFAULT NULL,
  shareholders varchar(500) DEFAULT NULL COMMENT '股东信息',
  gov_url varchar(200) DEFAULT NULL COMMENT '取信息的url参数',
  orgtype varchar(50) DEFAULT NULL COMMENT '组织形式',
  PRIMARY KEY (id,name),
  UNIQUE KEY name (name)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;
"""

#省市简写标识
SF_DIST = {'bj':'北京','gd':'广东','sd':'山东','zj':'浙江','js':'江苏','sh':'上海','ln':'辽宁','sc':'四川','ha':'河南','hb':'湖北','fj':'福建','hn':'湖南','he':'河北','cq':'重庆','sx':'山西','jx':'江西','sn':'陕西','ah':'安徽','hl':'黑龙江','gx':'广西','jl':'吉林','yn':'云南','tj':'天津','nm':'内蒙','xj':'新疆','gs':'甘肃','gz':'贵州','hi':'海南','nx':'宁夏','qh':'青海','xz':'西藏','hk':'香港'}

#各省市业务配置
BIZ_INFO={
		 'js':{'mod':'jiangsu'},
		 'cq':{'mod':'chongqing','thread_count':50},
		 'ah':{'mod':'anhui','thread_count':50},
		 'tj':{'mod':'tianji','thread_count':50},
		 'gx':{'mod':'anhui','thread_count':50,
		 		'urls':{'host':'http://gxqyxygs.gov.cn',
		 				'url_home':'http://gxqyxygs.gov.cn/search.jspx',
		 				'url_code':'http://gxqyxygs.gov.cn/validateCode.jspx?type=1&id=%s',
		 				'url_check':'http://gxqyxygs.gov.cn/checkCheckNo.jspx',
		 				'url_list':'http://gxqyxygs.gov.cn/searchList.jspx'}
		 },
		 'ha':{'mod':'anhui','thread_count':50,
		 		'urls':{'host':'http://222.143.24.157',
		 				'url_home':'http://222.143.24.157/search.jspx',
		 				'url_code':'http://222.143.24.157/validateCode.jspx?type=1&id=%s',
		 				'url_check':'http://222.143.24.157/checkCheckNo.jspx',
		 				'url_list':'http://222.143.24.157/searchList.jspx'}
		 },
		 'hl':{'mod':'anhui','thread_count':50,
		 		'urls':{'host':'http://gsxt.hljaic.gov.cn',
		 				'url_home':'http://gsxt.hljaic.gov.cn/search.jspx',
		 				'url_code':'http://gsxt.hljaic.gov.cn/validateCode.jspx?type=1&id=%s',
		 				'url_check':'http://gsxt.hljaic.gov.cn/checkCheckNo.jspx',
		 				'url_list':'http://gsxt.hljaic.gov.cn/searchList.jspx'}
		 },
		 }

if __name__=="__main__":

	dbinfo ={'host':'192.168.10.126','port':3306,'dbname':'gov_corp',
            'user':'wbsp','passwd':'wbsp','charset':'utf8'}
	mysqlwrap.setup_db('default',dbinfo)
	mysqlwrap.get_db().connect()
	rediswrap.setup_redis('default','192.168.10.126',6380)
	for p in SF_DIST.keys():
		sql = Data_tb % p
		mysqlwrap.get_db().query(sql,1)
	#print(get_proxy())
