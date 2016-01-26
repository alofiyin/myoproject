# -*- coding: utf-8 -*-
#Copyright  2015/8/21  fiyin
import mysqlwrap
import rediswrap
import time
import random
import datamodel
from threading import Thread
from eventlet.green import socket 
import eventlet
import traceback
queue_threshold = 2000 #队列阀值
rows_limit      = 1000  #每次从数据库获取记录数
#省市简写标识
SF_Dist = {'bj':'北京','gd':'广东','sd':'山东','zj':'浙江','js':'江苏','sh':'上海','ln':'辽宁','sc':'四川','ha':'河南','hb':'湖北','fj':'福建','hn':'湖南','he':'河北','cq':'重庆','sx':'山西','jx':'江西','sn':'陕西','ah':'安徽','hl':'黑龙江','gx':'广西','jl':'吉林','yn':'云南','tj':'天津','nm':'内蒙','xj':'新疆','gs':'甘肃','gz':'贵州','hi':'海南','nx':'宁夏','qh':'青海','xz':'西藏','hk':'香港'}

def savedata(data,table):
	"""保存数据到mysql数据库
	"""
	db = mysqlwrap.get_db()
	fields = []
	values = []
	for k,v in data.items():
		fields.append(k)
		#v = db.escape_string(v)
		v=v.replace('"'," ")
		values.append('"%s"' % v)
	sql = "insert into data_%s(%s)values(%s)" % (table,','.join(fields),','.join(values))

	res,desc = db.query(sql,1)
	return (res,desc)
	
def exist_corp(name,table):
	"""检查公司数据是否已存在
	"""
	db = mysqlwrap.get_db()
	sql = "select id from %s where name='%s'" %(table,name)
	res,desc = db.query(sql)
	if res == 0 and desc:
		return True
	return False
	
def queue_mnt():
	"""公司称名数据分配进程。
	公司名称的基本数据表命名格式 base_省份简称。
	自动提取以base_为前缀的公司基本表中的数据当对应的队列元素小于
	设定的阀值queue_threshold时。
	   
	"""
	db  = mysqlwrap.get_db()
	index_rd = rediswrap.get_hash('wbsp:gov:baseindex')
	while 1:
		try:
			sql = "SHOW TABLES LIKE 'base_%'"
			res, desc = db.query(sql)
			if res==0 and desc:
				for row in desc:
					tb = list(row.values())[0]
					q  = rediswrap.get_queue('wbsp:gov:queue.%s'%tb)
					#print('tb:%s q_len:%s' % (tb,q.__len__()))
					if q.__len__() >= queue_threshold:
						continue
					index = index_rd.get(tb,0)
					#print('tb:%s index:%s' % (tb,index))
					sql = "select id,name from %s where id >%s limit %s" % (tb,index,rows_limit)
					#print(sql)
					rs, ds = db.query(sql)
					if rs==0 and ds:
						id = 0
						for d in ds:
							id = d['id']
							q.push(d['name'])
						index_rd.set(tb,id)
		except Exception as e:
			traceback.print_exc()	
						
		time.sleep(10)

def exist_corp(name,table):
	"""检查公司数据是否已存在
	"""
	db = mysqlwrap.get_db()
	sql = "select id from %s where name='%s'" %(table,name)
	res,desc = db.query(sql)
	if res == 0 and desc:
		return True
	return False

				
def exec_main_proxy(mode):
	"""业务线程启动函数
	参数mod为业务模块
	模块工厂：
	mod.
	"""
	#socket.setdefaulttimeout(5)
	queue = datamodel.get_row_queue(mode.biz_flag)
	while 1:
		if datamodel.g_exit:
			break
		s_time=time.time()
		print(queue.__len__())	
		if queue.__len__() >0:
			proxyinfo = datamodel.get_proxy()
			#如果没有代理ip则插一个空值，使用本地ip
			if not proxyinfo:
				proxyinfo = ['']
			proxyinfo = set(proxyinfo)
			proxyinfo.difference_update(mode.ille_proxy_ip)
			#proxyinfo.add('')
			if len(proxyinfo) >mode.g_step:
				proxyinfo=random.sample(proxyinfo,mode.g_step)
			else:
				proxyinfo = list(proxyinfo)
			corps = []
			
			i = 0
			if not proxyinfo:
				print("not proxy ip....")
				time.sleep(5)
			print("start...")
			while i < len(proxyinfo):				
				corp = queue.pop(1)
				if not corp:					
					break
				if exist_corp(corp,mode.biz_flag):
					print(corp)
					continue
				corps.append(corp)
				i+=1
			proxyinfo = proxyinfo[:len(corps)]
			pool = eventlet.GreenPool(len(proxyinfo))
			result={}
			for corp,info,status,proxy in pool.imap(mode.get_info,corps,proxyinfo):
				if status in result:
					result[status]+=1
				else:
					result[status]=0
				if info and status==0:
					res,desc = savedata(info,mode.biz_flag)
					if res == -1:
						info['table'] = 'data_%s'%mode.biz_flag
						datamodel.get_tmp_queue().push(info)
				elif  status ==1:
					mode.ille_proxy_ip.add(proxy)
					queue.push(corp)
				print(corp,info,status)
			print(len(proxyinfo))
			print(result)
			e_time=time.time()-s_time
			print("kill time:%s"%(e_time))
		else:
			time.sleep(5)
		
def exec_main(mode):
	"""业务线程启动函数
	参数mod为业务模块
	模块工厂：
	mod.
	"""
	x=0
	i=0
	queue = datamodel.get_row_queue(mode.biz_flag)
	while 1:
		if datamodel.g_exit:
			break
		corp = queue.pop(3)
		if not corp:
			time.sleep(5)
			continue
		try:	
	
			if exist_corp(corp,mode.biz_flag):
				print(corp)
				continue

			corp,info,status,proxy =mode.get_info(corp)
			x+=1
			if info and status==0:
				i+=1
				res,desc = savedata(info,mode.biz_flag)
				if res == -1:
					info['table'] = 'data_%s'%mode.biz_flag
					datamodel.get_tmp_queue().push(info)
			elif  status ==1:
					#mode.ille_proxy_ip.add(proxy)
				queue.push(corp)
			print(corp,info,status)
			print("i=%s,x=%s" %(i,x))
		except:
			traceback.print_exc()					
if __name__=="__main__":
	dbinfo ={'host':'192.168.10.126','port':3306,'dbname':'gov_corp',
            'user':'wbsp','passwd':'wbsp','charset':'utf8'}
	mysqlwrap.setup_db('default',dbinfo)
	mysqlwrap.pool_monitor()
	rediswrap.setup_redis('default','192.168.10.126',6380)
	img_decode_url="http://127.0.0.1:1983/imgcode/base"
	t=Thread(target=queue_mnt)
	t.setDaemon(True)
	t.start()
	from modules import jiangsu
	exec_main(jiangsu)