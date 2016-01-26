# -*- coding: utf-8 -*-
#Copyright  2015/8/21  fiyin
import mysqlwrap
import rediswrap
import datamodel
import traceback
from core import savedata

from threading import Thread
from signal import signal, SIGINT, SIG_IGN,SIGTERM ,SIGCHLD


class DataMnt(Thread):
	def __init__(self):
		super().__init__()
	def run(self):
		db = mysqlwrap.get_db()
		queue = datamodel.get_tmp_queue()
		while 1:
			try:
				row = queue.pop(3)
				if row:
					tb = row.pop('table')[-2:]
					res,desc = savedata(row,tb)

					if desc:
						print(tb,res,desc)
			except:
				traceback.print_exc()
#–≈∫≈¥¶¿Ì
def sig_exit(a,b):

	os._exit(0)

if __name__=="__main__":
	signal(SIGINT,sig_exit)
	signal(SIGTERM,sig_exit)	
	dbinfo ={'host':'192.168.10.126','port':3306,'dbname':'gov_corp',
            'user':'wbsp','passwd':'wbsp','charset':'utf8'}
	mysqlwrap.setup_db('default',dbinfo)
	mysqlwrap.pool_monitor()	
	rediswrap.setup_redis('default','192.168.10.126',6380)
	d = DataMnt()
	d.run()				