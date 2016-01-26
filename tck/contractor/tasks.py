# -*- encoding: utf-8 -*-
from  task_reg_model import reg_task
import json
#import task_reg_model


#--------违法关键词过滤-----------
args = '{"input#输入配置": {"dbserver#数据库连接标识": "mysql:local_127_3354", "data#提取数据配置": {"dbname#数据库名": "biz72_company", "fields#要过滤的字段,必需包含id字段": "id,com_name,com_gsjj","where#条件":"", "table#表名": "com_corp","split_type#工作站分配方式 1 id范围|2 id取余":2, "range#id范围": [1, 1000], "weight#字段权重": {"com_name": 3, "com_gsjj": 2}}}, "output#输出配置": {"dbserver#数据库连接标识": "mysql:local_126_3306","weight#输出权重":0, "istest#是否为测试": true, "table#表名": "kw_illegal_records", "dbname#数据库名": "admincenter"}, "kwsource#违法词库配置": {"dbserver#数据库连接标识": "mysql:local_126_3306", "data#数据配置": {"dbname#数遍库名": "admincenter", "fields#字段": "k_word,g.k_weight", "table#表名": "kw_keywords_level as g,kw_keywords as k", "where#条件": "k_level=g.id"}}, "powerlevel#占用cpu等级low|mid|high|power": "low"}'
info={}
info['alias']='违法关键词过滤'
info['note']='违法关键词过滤'
info['args']=json.loads(args)

@reg_task(info=info)
def illegal_records(*ag, **kw):
    from modules import illegal_records
    return illegal_records.run(*ag, **kw)

info = "违法关键词过滤回回调函数，合并处理结果"
@reg_task
def  illegal_records_callback(kw):
	from modules import illegal_records
	illegal_records.callback(kw)

#--------代理ip自动抓取------------
info={}
info['alias']='抓取代理ip'
info['note']='从网上抓取公布的免费代理ip'
info['args']='{"urls":["http://ip.qiaodm.com/api.html?order=2456373454456&num=500&protocol=1&isp=0&distinct=0&an1=1&an2=1"]}' 
@reg_task(info=info)
def get_proxy(*ag, **kw):
	from modules import simpe
	return simpe.run('get_proxy',**kw)
	
info={}
info['alias']='检测可用代理IP'
info['note']='检测生产表的代理IP是否仍有效'
info['args']='' 
@reg_task(info=info)
def proxy_check_prod(*ag, **kw):
	from modules import simpe
	return simpe.run('proxy_check_prod',**kw)
	
info={}
info['alias']='清理代理ip缓存'
info['note']='清理失效的代理IP'
info['args']='' 
@reg_task(info=info)
def proxy_clean(*ag, **kw):
	from modules import simpe
	return simpe.run('proxy_clean',**kw)