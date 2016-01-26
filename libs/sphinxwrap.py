#_*_coding:utf-8_*_
#$Id: sphinx_class.py 3316 2015-03-01 13:27:53Z klirichek $
# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
#搜索引擎管理操作类操作类
# All rights reserved
__author__ = 'fiyin <alofiyin@gmail.com>'
__version__ = '$Revision: 0.1 $'

import pdb
from  sphinxapi import *

class sphinx(SphinxClient):
    def __init__(self,ip,port):
        #super(sphinx, self).__init__()
        SphinxClient.__init__(self)
        self.ip = ip
        self.port = port
        self.searchMax = 1000
    def initQuery(self,item):
        #pdb.set_trace()
        #设置搜索服务￱
        self.SetServer(self.ip, self.port)
        #设置超时时间
        self.SetConnectTimeout(20.0)
        #以下设置用于返回数组形式的结果￻
        #self.SetArrayResult(true)
        #设置评分模式
        self.SetRankingMode(SPH_RANK_PROXIMITY_BM25)
        #设置匹配模式
        '''
        SPH_MATCH_ALL,匹配所有查询词(默认模式);
        SPH_MATCH_ANY,匹配查询词中的任意一个;
        SPH_MATCH_PHRASE, 将整个查询看作一个词组，要求按顺序完整匹配;
        SPH_MATCH_BOOLEAN, 将查询看作一个布尔表达式 (参见 Section 4.2, "布尔查询语法");
        SPH_MATCH_EXTENDED, 将查询看作一个Sphinx/Coreseek内部查询语言的表达式 (参见 Section 4.3, "扩展查询语法"). 从版本Coreseek 3/Sphinx 0.9.9开始, 这个选项被选项SPH_MATCH_EXTENDED2代替，它提供了更多功能和更佳的性能。保留这个选项是为了与遗留的旧代码兼容——这样即使Sphinx及其组件包括API升级的时候，旧的应用程序代码还能够继续工作。
        SPH_MATCH_EXTENDED2, 使用第二版的"扩展匹配模式"对查询进行匹配.
        SPH_MATCH_FULLSCAN, 强制使用下文所述的"完整扫描"模式来对查询进行匹配。注意，在此模式下，所有的查询词都被忽略，尽管过滤器、过滤器范围以及分组仍然起作用，但任何文本匹配都不会发生.
        '''
        if "querymod" in item and item["querymod"] :
            self.SetMatchMode(eval(str(item["querymod"])))
        else:
            self.SetMatchMode (SPH_MATCH_EXTENDED2)
        #设置分页
        
        if not 'pageSize' in item or not item['pageSize']:
            item['pageSize']=20
        if not 'page' in item or not item['page']:
            item['page'] = 1
        self.SetLimits((item['page']-1)*item['pageSize'],item['pageSize'],self.searchMax, 0)
        
        #整形的过滤
        if 'intType' in item and item['intType']:
            for k,v in item['intType'].items():
                self.SetFilter(str(k),list(map(int,v.split(','))),0)
                #self.SetFilter(k,v,0)
        #设置整形的范围
        if 'intRange' in item and item['intRange']:
            for k,v in item['intRange'].items():
                rangs = v.split(',');
                self.SetFilterRange(str(k),int(rangs[0]),int(rangs[1]),int(rangs[2]))    
                
        #设置浮点数的范围
        if 'floatRange' in item and item['floatRange']:
            for k,v in item['intType'].items():
                rangs = v.split(',');
                self.SetFilterFloatRange(str(k),float(rangs[0]),float(rangs[1]),int(rangs[2]))    
        #搜索引擎排序的设置
        if 'orderBy' in item and item['orderBy']:
            orderBy = item['orderBy'].split('|')
            self.SetSortMode(eval(str(orderBy[0])),str(orderBy[1]))
        
        #分组的设置, 只取分组的一条信息]
        if 'groupBy' in item and item['groupBy']:
            groupBy = item['groupBy'].split(',')
            self.SetGroupBy(str(groupBy[0]),eval(str(groupBy[1])),str(groupBy[2]))
            #分组后一个字段属性唯一性
            if 'groupDistinct' in item and item["groupDistinct"]:
                self.SetGroupDistinct(item["groupDistinct"])
        else:
            self.ResetGroupBy()
        
        #计算搜索字段的权值
        if 'weight' in item and item['weight']:
            self.SetFieldWeights (item['weight'])
            
        #关键字的所有设置
        keyw = ""
        if 'keyw' in item and item['keyw']:
            keyw = str(item['keyw'])
        self.AddQuery(keyw, str(item['index']))
        self.ResetFilters()

if __name__ == "__main__":
    item={'querymod':'SPH_MATCH_EXTENDED2', \
        'pageSize':0, \
        'page':1, \
        'intType':{\
            'r_tag_id':'101', 'status':'1', 'isimg':'1'
            },\
        'orderBy':'SPH_SORT_EXPR|FLOOR(log2(@weight))+mem_level*6+isimg*10+IDIV(pub_time,2592000)',\
        'groupBy':'com_id,SPH_GROUPBY_ATTR,isimg desc pub_time desc',\
        'weight':{'title':8,'com_name':4,'keyword':2},\
        'index':'IDX_pro_info_dist'    
        }
    #item={'orderBy': 'SPH_SORT_EXPR|FLOOR(log2(@weight))+mem_level*6+isimg*10+IDIV(pub_time,2592000)', 'index': 'IDX_pro_info_dist', 'intType': {'isimg': '1', 'status': '1', 'r_tag_id': '101'}, 'weight': {'com_name': 4, 'keyword': 2, 'title': 8}, 'pageSize': 30, 'page':1,             
    item={'orderBy': 'SPH_SORT_EXPR|FLOOR(log2(@weight))+mem_level*6+isimg*10+IDIV(pub_time,2592000)', 'index': 'IDX_com_info_dist', 'intType': {'isimg': '1', 'status': '1', 'r_tag_id': '101'}, 'weight': {'com_name': 4, 'keyword': 2, 'title': 8}, 'pageSize': 30, 'keyw': [], 'page': 1, 'querymod': 'SPH_MATCH_EXTENDED', 'groupBy': 'com_id,SPH_GROUPBY_ATTR,isimg desc pub_time desc'}
    s = sphinx('192.168.0.133',9402)
    for i in [101,101101]:
        tmp = item.copy()
        tmp['intType']['r_tag_id'] = str(i)
        s.initQuery(tmp)
    
    res = s.RunQueries()
    pdb.set_trace()
    print(res)