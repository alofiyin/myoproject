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
from queue import Queue
import setproctitle
import config 
import logging

logger = logging.getLogger('main')
QUEUE_THRESHOLD = 2000  #队列阀值
ROWS_LIMIT      = 1000  #每次从数据库获取记录数
THREAD_COUNT    = 100    #线程数
PROCESS_DIST    = {}    #线程池
REPORT_TIME     =120    #报告进度时间间隔



def savedata(data,table):
	"""保存数据到mysql数据库
	"""
	db = mysqlwrap.get_db()
	if type(data) != list:
		data = [data]
	for item in data:
		fields = []
		values = []
		for k,v in item.items():
			fields.append(k)
			v=mysqlwrap.addslashes(v)
			values.append('"%s"' % v)
		sql = "insert into data_%s(%s)values(%s)" % (table,','.join(fields),','.join(values))
		res,desc = db.query(sql,1)
		#print(sql,res,desc)
		#数据入库失败处理
		if res == -1:
			#print('insert_error:',desc)
			if desc.args[0] in [1064,1062]:
				return (0,())
			item['table'] = 'data_%s'%table
			datamodel.get_tmp_queue().push(item)
		#插入dat_total总表
		#print(item)
		if 'reg_status' in item and item['reg_status'] in ['存续','在业'] :
			fields.append('prov_tb')
			values.append('"%s"' % table)
			t_table = 'data_total'
			
			sql = "insert into %s(%s)values(%s)" % (t_table,','.join(fields),','.join(values))
			rs,ds = db.query(sql,1)
			#print("insert total tb",rs,ds)
	return (res,desc)

def updata(data,table):
	"""更新数据
	"""
	db = mysqlwrap.get_db()
	if type(data) != list:
		data = [data]	
	for item in data:
		for k,v in item.items():
			v=mysqlwrap.addslashes(v)
			item[k]=v
		where = "name='%s'" % item['name']
		res,desc = db.update("data_%s" % table,item,where)
		#数据入库失败处理
		if 'reg_status' in item and item['reg_status'] in ['存续','在业','存续（在营、开业、在'] :
			item['prov_tb']='"%s"' % table
			t_table = 'data_total'
			res,desc = db.update(t_table,item,where)
			print("insert total tb",res,desc)
	return (res,desc)	
	
def chang_flag(corp,flag,table):
	"""更改原始公司表中的flag
	"""
	db = mysqlwrap.get_db()
	sql = "update  base_%s set flag=%s where name='%s'" % (table,flag,corp)
	res,desc = db.query(sql,1)
	#print("chang_flag:",res,desc)
def check_exist_corp(biz):
	"""对比数据表
	"""
	res,desc = mysqlwrap.get_db().query("select max(id) as mx,min(id) as mi from base_%s" % biz)

	mx = desc[0]['mx']
	mi = desc[0]['mi']
	while mi <=mx:
		step = mi + 1000
		sql = "select name from base_%s where id >%s and id <%s" %(biz,mi,step)
		res,desc = mysqlwrap.get_db().query(sql)
		for row in desc:
			s = "select id from data_%s where name='%s'" % (biz,row['name'])
			rs,ds = mysqlwrap.get_db().query(s)
			if rs==0 and ds:
				sql = "update base_%s set flag=1 where name='%s'" % (biz,row['name'])
				result = mysqlwrap.get_db().query(sql,1)
				#print(result)
		mi=step
						
def exist_corp(name,table):
	"""检查公司数据是否已存在
	"""
	db = mysqlwrap.dbclass(config.CONFIG['mysqld'])
	db.connect()
	sql = "select id from data_%s where name='%s'" %(table,name)
	res,desc = db.query(sql)
	#print('DB: ',res,desc)
	db.close()
	if res == 0 and desc:
		return True
	
	return False


def stat_tabls_rows(tb_prefix):
	"统计同一前缀的表记录数"	
	db  = mysqlwrap.get_db()
	sql = "SHOW TABLES LIKE '"+tb_prefix+"%'"

	res, desc = db.query(sql)
	totel=0
	if res==0 and desc:
		for row in desc:
			tb = list(row.values())[0]
			sql = "select count(0) as n from %s" % tb
			rs, ds = db.query(sql)
			if rs ==0 and ds:
				totel+=ds[0]['n']
				print(tb,ds[0]['n']) 
	print("totel:%s" % totel)

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
					id = 0
					tb = list(row.values())[0]
					q  = rediswrap.get_queue('wbsp:gov:queue.%s'%tb)
					#print('tb:%s q_len:%s' % (tb,q.__len__()))
					if q.__len__() >= QUEUE_THRESHOLD:
						continue
					index = index_rd.get(tb,0)
					#print('tb:%s index:%s' % (tb,index))
					sql = "select id,name,flag from %s where id >%s limit %s" % (tb,index,ROWS_LIMIT)
					#print(sql)
					rs, ds = db.query(sql)
					if rs==0 and ds:
						
						for d in ds:
							if d['flag'] >0 or d['flag'] <0:
								continue
							id = d['id']
							q.push(d['name'])
						index_rd.set(tb,id)

		except Exception as e:
			traceback.print_exc()	
						
		time.sleep(10)

def push_proxy_queue(q,ille_proxy_ip,size=10):
	"""补充代理ip队列
	"""
	if q.qsize() <size:
		proxy = datamodel.get_proxy()
		proxy = set(proxy)
		proxy.difference_update(ille_proxy_ip)
		for p in proxy:
			q.put(p)
						
class ExecThread(Thread):
	"""业务线程启动函数
	参数mod为业务模块
	模块工厂：
	mod.
	"""
	def __init__(self,mode,queue):
		super(ExecThread,self).__init__()
		self.mode=mode
		self.q =queue
		self.exit_flag = False
	def run(self):
		#socket.setdefaulttimeout(5)
		#计时器
		t_count = int(time.time())
		queue = datamodel.get_row_queue(self.mode.biz_flag)
		#代理ip存活标识
		proxyip_isAlive = False
		#慢速代理ip集合
		proxyslowip     = set()
		while not self.exit_flag:
			if datamodel.g_exit:
				break
			try:
				corp = queue.pop(1)
			except:
				corp = ""
				time.sleep(5)
			if not corp:
				continue
			#检查公司是否已存在
			#if exist_corp(corp,self.mode.biz_flag):
				#print("exist_corp:%s" % corp)
			#	continue
	
			#print(queue.__len__())
			
			#到时间清空慢速代理ip集合
			if (int(time.time())- t_count) > 60 :
				proxyslowip     = set()
				t_count = int(time.time())	
			#获取代理ip
			if not proxyip_isAlive:
				#如果没有代理ip则插一个空值，使用本地ip
				while 1:
					if datamodel.g_exit:
						break
					if self.q.qsize() ==0:
						time.sleep(1)
						continue
					try:
						proxyinfo = self.q.get()
					except:
						proxyinfo=""
						
					if proxyinfo in proxyslowip:
						continue
					break	
				
			s_time = time.time()							
			corp,info,status,proxy = self.mode.get_info(corp,proxyinfo)
	
			if info and status==0:
				#print(corp,info,status,proxy)
				self.mode.Ok_num+=1
				savedata(info,self.mode.biz_flag)
				proxyip_isAlive=True
				chang_flag(corp,1,self.mode.biz_flag)
			elif  status ==1:	
				self.mode.False_num+=1
				proxyip_isAlive=False	
				proxyslowip.add(proxy)
				queue.push(corp)
			elif status ==2:
				self.mode.False_num+=1
				proxyip_isAlive=False
				queue.push(corp)
			else:
				self.mode.Null_num+=1
				chang_flag(corp,-1,self.mode.biz_flag)
				proxyip_isAlive=True
			print(corp,info,status,proxy)
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
				
				continue

			corp,info,status,proxy =mode.get_info(corp)
			x+=1
			if info and status==0:
				#print(corp,info,status,proxy)
				mode.Ok_num+=1
				savedata(info,mode.biz_flag)
				chang_flag(corp,1,mode.biz_flag)
			elif  status ==1:	
				mode.False_num+=1
				queue.push(corp)
			elif status ==2:
				mode.False_num+=1
				queue.push(corp)
			else:
				mode.Null_num+=1
				chang_flag(corp,-1,mode.biz_flag)
			print(corp,info,status,proxy)
			#print("i=%s,x=%s" %(i,x))
		except:
			traceback.print_exc()	
			
def start_thread(kw):
	"""执行任务
	"""
	#注册数据库
	mysqlwrap.setup_db('default',config.CONFIG['mysqld'])
	#启动数据连接池守护进程
	mysqlwrap.pool_monitor()
	thread_count = kw.pop('thread_count',THREAD_COUNT)
	biz_flag     = kw.pop('biz_flag')
	exit_flag    = kw.get('exit_flag')
	urls         = kw.get('urls','')
	if biz_flag not in  datamodel.SF_DIST.keys():
		raise Exception("illegal biz_flag!")
	mod          = kw.pop('mod')

				
	#设置进程名
	title = "%s %s %s" %(datamodel.proc_title,mod,biz_flag)
	setproctitle.setproctitle(title)
	logger.info("%s start..." % title)
	prox_queue = Queue()
	try:		
		md = __import__(mod)
		md.biz_flag = biz_flag
		if urls:
			for k,url in urls.items():
				exec("md.%s='%s'" % (k,url))
			print(urls)
		thrd = [ExecThread(md,prox_queue) for i in range(0,thread_count)]
		#thrd.append(Thread(target=exec_main,args=(md,)))
		for i in range(0,len(thrd)):
			thrd[i].setDaemon(True)
			thrd[i].start()
	except Exception as e:
		traceback.print_exc()	
	s_time = time.time()
	while 1:
		#填充代理ip队列
		push_proxy_queue(prox_queue,md.ille_proxy_ip)
		if 	exit_flag.is_set():
			logger.info("%s exit..." % title)
			datamodel.g_exit = True
			for i in range(0,len(thrd)):
				#print(thrd[i].name + "exit....")
				thrd[i].stop()
				thrd[i].join()
			break
		for i in range(0,len(thrd)):
			if not thrd[i].isAlive():
				#print("%s is death try reload..." % thrd[i].name)
				thrd[i] = ExecThread(md,prox_queue)
				thrd[i].setDaemon(True)
				thrd[i].start()
		if int(time.time())-s_time > REPORT_TIME:
			logger.info("%s %s S:%s N:%s F:%s" % (mod,biz_flag,md.Ok_num,md.Null_num,md.False_num))
			s_time = time.time()
		time.sleep(3)

def start_proc(kw):
	"""启动任务进程
	kw={}
	kw['biz_flag'] = 'js'  省份标识
	kw['exit_flag']= mp.Event() 退出事件
	kw['mod'] = 'jiangsu'    业务模块名
	kw['thread_count']=100   开启线程数
	"""
	p=mp.Process(target=start_thread, args=(kw,))
	p.daemon = True
	p.start()
	PROCESS_DIST[kw['biz_flag']]={'kw':kw,'p':p}		
	
class MainMnt(Thread):
	"""启动主线程
	"""	
	def __init__(self):
		super(MainMnt,self).__init__()
	
	def run(self):
		
		for biz,info in datamodel.BIZ_INFO.items():
			if 'mod' not in info:
				continue
			info['exit_flag'] = mp.Event()
			info['biz_flag'] = biz
			start_proc(info)
			time.sleep(1)
		i=0	
		while 1:
			if datamodel.g_exit:
				self.finish()
				break

			time.sleep(1)
	def finish(self):
		for biz in PROCESS_DIST.keys():
			PROCESS_DIST[biz]['kw']['exit_flag'].set()
			PROCESS_DIST[biz]['p'].join()		
						
if __name__=="__main__":
	

	#dbinfo ={'host':'192.168.10.126','port':3306,'dbname':'gov_corp',
    #        'user':'wbsp','passwd':'wbsp','charset':'utf8'}

	#check_exist_corp('js')
	config.read('./conf/worker.conf')
	mysqlwrap.setup_db('default',config.CONFIG['mysqld'])
	mysqlwrap.pool_monitor()
	THREAD_COUNT = 10
	import sys
	sys.path.append(sys.path[0]+'/modules')
	rediswrap.setup_redis('default','192.168.10.126',6380)
	#stat_tabls_rows('base_')
	'''
	import jiangsu
	thr = Thread(target=exec_main,args=(jiangsu,))
	thr.setDaemon(True)
	thr.start()
	'''
	kw={}
	kw['biz_flag'] = 'tj'
	kw['exit_flag']= mp.Event()
	kw['mod'] = 'tianji'
	kw['thread_count']=1
	p=mp.Process(target=start_thread, args=(kw,))
	p.daemon = True
	p.start()
	i=0
	while 1:
		time.sleep(1)
		print(i)
		i+=1
		if i >300:
			kw['exit_flag'].set()
			print("now exiting...")
			p.join()
			break
			 

