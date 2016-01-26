# -*- encoding: utf-8 -*-
from  jobs_reg_mode import reg_job
import threading
info = "这是一个测试函数"
@reg_job(note=info)
def test(a,b):
    print("hole !!")

info = "违法关键词过滤"
@reg_job(note=info)
def words_for_db(*ag, **kw):
    from modules.words.wordsfordb import WordsForDB
    job = WordsForDB(*ag, **kw)
    job.setDaemon(True)
    job.start()

#--------代理ip自动抓取------------
info={}
info['alias']='抓取代理ip'
info['note']='从网上抓取公布的免费代理ip'
info['args']='' 
@reg_job(info=info)
def get_proxy(*ag, **kw):
	from modules.net import proxyip
	t=threading.Thread(target=proxyip.get_proxy,args=[kw,])
	t.setDaemon(True)
	t.start()
	
info={}
info['alias']='检测可用代理IP'
info['note']='检测生产表的代理IP是否仍有效'
info['args']='' 
@reg_job(info=info)
def proxy_check_prod(*ag, **kw):
	from modules.net import proxyip
	t=threading.Thread(target=proxyip.proxy_check_prod,args=[kw,])
	t.setDaemon(True)
	t.start()	
info={}
info['alias']='清理代理ip缓存'
info['note']='清理失效的代理IP'
info['args']='' 
@reg_job(info=info)
def proxy_clean(*ag, **kw):
	from modules.net import proxyip
	t=threading.Thread(target=proxyip.clean,args=[kw,])
	t.setDaemon(True)
	t.start()