# -*- coding: utf-8 -*-
#Copyright  2015/8/21  fiyin
import mysqlwrap
import rediswrap
import time
import random
import datamodel
from threading import Thread
import socket 
import traceback
import multiprocessing as mp

QUEUE_THRESHOLD = 2000  #队列阀值
ROWS_LIMIT      = 1000  #每次从数据库获取记录数
THREAD_COUNT    = 50    #线程数
PROCESS_DIST    = {}    #时程池

#省市简写标识
SF_DIST = {'bj':'北京','gd':'广东','sd':'山东','zj':'浙江','js':'江苏','sh':'上海','ln':'辽宁','sc':'四川','ha':'河南','hb':'湖北','fj':'福建','hn':'湖南','he':'河北','cq':'重庆','sx':'山西','jx':'江西','sn':'陕西','ah':'安徽','hl':'黑龙江','gx':'广西','jl':'吉林','yn':'云南','tj':'天津','nm':'内蒙','xj':'新疆','gs':'甘肃','gz':'贵州','hi':'海南','nx':'宁夏','qh':'青海','xz':'西藏','hk':'香港'}


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

	#数据入库失败处理
	if res == -1:
		if desc.args[0] == 1064:
			print(desc)
			return
		data['table'] = 'data_%s'%table
		datamodel.get_tmp_queue().push(data)
	#return (res,desc)
	
def exist_corp(name,table):
	"""检查公司数据是否已存在
	"""
	db = mysqlwrap.get_db()
	sql = "select id from data_%s where name='%s'" %(table,name)
	res,desc = db.query(sql)
	print(res,desc)
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
			if datamodel.g_exit:
				break
			#检查公司队列
			sql = "SHOW TABLES LIKE 'base_%'"
			res, desc = db.query(sql)
			if res==0 and desc:
				for row in desc:
					tb = list(row.values())[0]
					q  = rediswrap.get_queue('wbsp:gov:queue.%s'%tb)
					#print('tb:%s q_len:%s' % (tb,q.__len__()))
					if q.__len__() >= QUEUE_THRESHOLD:
						continue
					index = index_rd.get(tb,0)
					#print('tb:%s index:%s' % (tb,index))
					sql = "select id,name from %s where id >%s limit %s" % (tb,index,ROWS_LIMIT)
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

def push_proxy_queue(q,size=10):
	"""补充代理ip队列
	"""
	if q.qsize <size:
		proxy = datamodel.get_proxy()
		for p in proxy:
			q.put(p)
						
class ExecThread(Thread):
	"""业务线程启动函数
	参数mod为业务模块
	模块工厂：
	mod.
	"""
	def __init__(self,mode):
		super(ExecThread,self).__init__()
		self.mode=mode
		self.exit_flag = False
	def run(self):
		#socket.setdefaulttimeout(5)
		queue = datamodel.get_row_queue(self.mode.biz_flag)
		#代理ip存活标识
		proxyip_isAlive = False
		proxyslowip     = set()
		while not self.exit_flag:
			if datamodel.g_exit:
				break
			corp = queue.pop(1)
			if not corp:
				continue
			#检查公司是否已存在
			if exist_corp(corp,self.mode.biz_flag):
				#print("exist_corp:%s" % corp)
				continue
	
			s_time=time.time()
	
			#print(queue.__len__())	
			#获取代理ip
			if not proxyip_isAlive:
				proxyinfo = datamodel.get_proxy()
					#如果没有代理ip则插一个空值，使用本地ip
				if not proxyinfo:
					proxyinfo = ['']
				proxyinfo = set(proxyinfo)
				plen = len(proxyinfo)
				proxyinfo.difference_update(self.mode.ille_proxy_ip,proxyslowip)
					#proxyinfo.add('')
				if plen >5 and len(proxyinfo) <5:
					 proxyslowip=set()
				proxyinfo=random.sample(proxyinfo,1)
							
			#如果没有ip可用，挂起
			if not proxyinfo:
					print("not proxy ip....")
					time.sleep(5)
					continue				
			corp,info,status,proxy = self.mode.get_info(corp,proxyinfo[0])
	
			if info and status==0:
				print(corp,info,status,proxy)
				savedata(info,self.mode.biz_flag)
				proxyip_isAlive=True
			elif  status ==1:	
				proxyip_isAlive=False	
				proxyslowip.add(proxy)
				queue.push(corp)
			elif status ==2:
				proxyip_isAlive=False
				queue.push(corp)
			else:
				proxyip_isAlive=True
			#print(corp,info,status,proxy)
			e_time=time.time()-s_time
			#print("kill time:%s"%(e_time))
		else:
			time.sleep(5)
	def stop(self):
		self.exit_flag = True
		
			
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
			print(corp,info,status,proxy)
			print("i=%s,x=%s" %(i,x))
		except:
			traceback.print_exc()	
			
def start_thread(kw):
	"""执行任务
	"""
	thread_count = kw.pop('thread_count',THREAD_COUNT)
	biz_flag     = kw.pop('biz_flag')
	exit_flag    = kw.get('exit_flag')
	if biz_flag not in  SF_DIST.keys():
		raise Exception("illegal biz_flag!")
	mod          = kw.pop('mod')
	try:		
		md = __import__(mod)
		md.biz_flag = biz_flag
		thrd = [ExecThread(md) for i in range(0,thread_count)]
		for i in range(0,len(thrd)):
			thrd[i].setDaemon(True)
			thrd[i].start()
	except Exception as e:
		traceback.print_exc()	
	while 1:
		if 	exit_flag.is_set():
			print("exit procession...")
			for i in range(0,len(thrd)):
				thrd[0].stop()
				thrd[0].join()
			break
		for i in range(0,len(thrd)):
			if not thrd[i].isAlive():
				print("%s is death try reload..." % thrd[i].name)
				thrd[i] = ExecThread(md)
				thrd[i].setDaemon(True)
				thrd[i].start()
		time.sleep(3)
					
if __name__=="__main__":
	

	dbinfo ={'host':'192.168.10.126','port':3306,'dbname':'gov_corp',
            'user':'wbsp','passwd':'wbsp','charset':'utf8'}
	mysqlwrap.setup_db('default',dbinfo)
	mysqlwrap.pool_monitor()
	
	import sys
	sys.path.append(sys.path[0]+'/modules')
	rediswrap.setup_redis('default','192.168.10.126',6380)
	img_decode_url="http://127.0.0.1:1983/imgcode/base"
	kw={}
	kw['biz_flag'] = 'js'
	kw['exit_flag']= mp.Event()
	kw['mod'] = 'jiangsu'
	kw['thread_count']=100
	p=mp.Process(target=start_thread, args=(kw,))
	p.daemon = True
	p.start()
	i=0
	while 1:
		time.sleep(1)
		i+=1
		if i >60:
			kw['exit_flag'].set()
			print("now exiting...")
			p.join()
			break
			 
