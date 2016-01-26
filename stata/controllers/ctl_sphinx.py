#_*_coding:utf-8_*_
#
#sphinx 查询代理
#
from sphinxwrap import sphinx
from stat_base import get_cnf_val,get_host_by_data,err_handle
import sconf
def proxy(kw):
    """
    param=[
            {'querymod':'SPH_MATCH_EXTENDED2', \
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
         ]
    """
    param = kw.pop("param",[])
    #检查主参数
    if not param:
        return err_handle.sphinx_param_not_set
    #检查索引
    if 'index' not in param[0]:
        return err_handle.sphinx_index_not_found
    index = "base.sphinx.%s" % param[0]['index']
    #检查索引对应的搜索服务器是否存在   
    host_info = get_host_by_data(index)
    if  not host_info :
        return err_handle.sphinx_index_not_found
    #连接搜索引擎
    sp = sphinx(host_info['host'],host_info['port'])
    #加载query
    for q in param:
        sp.initQuery(q)
    res = sp.RunQueries()

    #返回结果
    return [0,res]
    
def get_index(kw):
	
    data = get_cnf_val('base.sphinx',sconf.DATA_SOURC)
    return [0,data]