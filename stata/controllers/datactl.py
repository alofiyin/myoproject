#_*_coding:utf-8_*_
#数据模型
from  sphinxwrap import sphinx
import json, time
import eventlet
from threading import Thread
#from  sphinxapi import *
def test1(*ag,**kw):
    t=int(time.time())
    tmp ='牛宝'
    item={'querymod':'SPH_MATCH_EXTENDED2', \
        'pageSize':1, \
        'page':1, \
        #'intType':{\
         #'status':'1', 'isimg':'1'
        #    },\
        #'intRange':{\
        #	'province':'101101,101111,0',
        #    'city':'101101101,109102101,0'},
        #'orderBy':'SPH_SORT_EXPR|FLOOR(log2(@weight))+mem_level*6+isimg*10+IDIV(pub_time,2592000)',\
        #'orderBy':'SPH_SORT_ATTR|pub_time desc' ,
        #'groupBy':'status,SPH_GROUPBY_ATTR,status desc',\
        #'weight':{'title':8,'com_name':4,'keyword':2},\
        'index':'IDX_pro_info_dist' , 
        #'keyw': '( "牛宝 百叶 牛鞭 在家 欧阳"/3)'
        }
    #item={'orderBy': 'SPH_SORT_EXPR|FLOOR(log2(@weight))+mem_level*6+isimg*10+IDIV(pub_time,2592000)', 'index': 'IDX_pro_info_dist', 'intType': {'isimg': '1', 'status': '1', 'r_tag_id': '101'}, 'weight': {'com_name': 4, 'keyword': 2, 'title': 8}, 'pageSize': 30, 'page':1,             
    #item={'orderBy': 'SPH_SORT_EXPR|FLOOR(log2(@weight))+mem_level*6+isimg*10+IDIV(pub_time,2592000)', 'index': 'IDX_pro_info_dist', 'intType': {'isimg': '1', 'status': '1', 'r_tag_id': '101'}, 'weight': {'com_name': 4, 'keyword': 2, 'title': 8}, 'pageSize': 30, 'keyw': [], 'page': 1, 'querymod': 'SPH_MATCH_EXTENDED', 'groupBy': 'com_id,SPH_GROUPBY_ATTR,isimg desc pub_time desc'}

    s = sphinx('192.168.10.127',9501)
    #s = sphinx('183.60.177.157',9501)
    #for i in [101,101101]:
    #    tmp = item.copy()
    #tmp['intType']['r_tag_id'] = str(i)
    s.initQuery(item)
    
    rs = s.RunQueries()
    if rs:
        res=rs[0]
    else:
        print(rs)
        return [s._error]

    print('useritme:',time.time()-t)
 
    #if res['status']==0:
    #    num+=1
    status=res['status'] if 'status' in res else -1
    _time=res['time'] if 'time' in res else 0
    total_found= res['total_found'] if 'total_found' in res else 0
    warning = res['warning'] if 'warning' in res else ''
    #print(res)
    return (status,_time,total_found,warning)    
def test(*ag,**kw):
    
    sp = SphinxClient()
    sp.SetServer('192.168.10.127',9501)
    sp.SetRankingMode(SPH_RANK_PROXIMITY_BM25)
    sp.SetMatchMode (SPH_MATCH_EXTENDED2)
    rs=sp.Query('( "牛宝 百叶 牛鞭 在家 欧阳"/3)','IDX_pro_info_dist')
    #rs = sp.RunQueries()
    if rs:
        res=rs[0]
    else:
        print(sp._error)
        return [sp._error]
 
    #if res['status']==0:
    #    num+=1
    status=res['status'] if 'status' in res else -1
    _time=res['time'] if 'time' in res else 0
    total_found= res['total_found'] if 'total_found' in res else 0
    warning = res['warning'] if 'warning' in res else ''
    #print(res)
    return (status,_time,total_found,warning)    
if __name__=="__main__":
    test()