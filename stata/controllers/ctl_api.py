#_*_coding:utf-8_*_
import stat_base
#------------------------
#group操作
#------------------------
def reg_group(kw):
	"""注册group
	"""
	if 'gkey' not in kw:
		return stat_base.err_handle.gkey_not_set
	if 'info' not in kw:
		return [-6,'缺失参数info']
	return stat_base.reg_group(kw['gkey'],kw['info'])
	
def get_groups(kw):
	"""提取group信息
	"""
	gkeys = kw.get('gkeys',[])
	
	return 	stat_base.get_groups(gkeys)	
	
def update_group(kw):
	if 'gkey' not in kw:
		return stat_base.err_handle.gkey_not_set
	if 'data' not in kw:
		return stat_base.err_handle.data_not_found
	return stat_base.update_group(kw['gkey'],kw['data'])	
#------------------------
#items操作
#------------------------
def reg_items(kw):
	"""注册items
	"""	
	if 'gkey' not in kw:
		return stat_base.err_handle.gkey_not_set
	if 'items' not in kw:
		return stat_base.err_handle.items_not_set
	prefix = kw.pop('prefix','') 	
	res,desc = stat_base.reg_items(kw['gkey'],kw['items'],prefix)
	#注册成功，写入redis缓存
	if res ==0:
		stat_base.reg_items2redis(kw['gkey'],[k[1] for k in kw['items']])
	return res,desc
	
def get_items(kw):
	"""提取items
	"""
	if 'gkey' not in kw:
		return stat_base.err_handle.gkey_not_set
	itms = kw.get('items',[])
	return 	stat_base.get_items(kw['gkey'],itms)
	
def update_item_key(kw):
	if 'gkey' not in kw:
		return stat_base.err_handle.gkey_not_set
	if 'oldkey' not in kw :
		return [-6,'缺失参数oldkey.']
	if 'newkey' not in kw:
		return [-6,'缺失参数newkey.']
	return stat_base.update_item(kw['gkey'],kw['oldkey'],kw['newkey'])
def update_item_name(kw):
	if 'gkey' not in kw:
		return stat_base.err_handle.gkey_not_set
	if 'itemkey' not in kw:
		return [-6,'缺失参数itemkey.']
	if 'name' not in kw:
		return [-6,'缺失参数name.']
	return stat_base.update_item_name(kw['gkey'],kw['itemkey'],kw['name'])
#------------------------
#history操作
#------------------------
def set(kw):
	"""上传值，先从redis缓存中取出item的id，再匹配itemkey入history库
	参数说明:
	gkey group 的gkey
	data 数据集
	  {'itemkey':{'value':值,'clock':生成时间，默认为当前时间戳}}
	"""
	if 'gkey' not in kw:
		return stat_base.err_handle.gkey_not_set
	if 'data' not in kw:
		return stat_base.err_handle.data_not_found
	res,desc = stat_base.set(kw['gkey'],kw['data'])
	if res <0:
		stat_base.reg_items2redis(kw['gkey'],list(kw['data'].keys()))
		return stat_base.set(kw['gkey'],kw['data'])
	else:		
		return 	res,desc
def send(kw):
	"""将统计数据在redis中累加
	"""
	if 'gkey' not in kw:
		return stat_base.err_handle.gkey_not_set
	if "data" not in kw:
		return stat_base.err_handle.data_not_found
	return stat_base.send(kw['gkey'],kw['data'])
	
		
def get(kw):
	"""	获取统计数据
	参数说明
	   itm itemid列表 为空时提取整个group的记录
	   start_time 开始时间戮
	   stop_time  结构时间戮
	   sort       排序方式 
	   groupby    分组方式 1 clock 2 itemid 3 1+2
	   page       分页参数集 {'site':每页数据量,'num':页码} 默认返回所有记录
    返回值:
     [names,items]   
     	names {'itemid':'itemname'}
     	items [{itemid,val,clock}]
	"""
	if 'gkey' not in kw:
		return stat_base.err_handle.gkey_not_set
	args = kw.get('args',{})
	return stat_base.get(kw['gkey'],**args)

def reg_items2redis(kw):
	if 'gkey' not in kw:
		return [-1,'gkey not set.']
	itms = kw.get('items',[])
	
	return 	stat_base.reg_items2redis(kw['gkey'],itms)			
	

	

if __name__=="__main__":
    '''
    #tset for reg_group:
    json = '{"gkey":"test01","info":{"name":"测试组01","pid":1}}'
    
    curl -l -H "Content-Type: application/json" -X POST -d '{"gkey":"test01","info":{"name":"测试组01","pid":1}}'  http://192.168.10.126:1985/api/reg_group
    
    curl -l -H "Content-Type: application/json" -X POST -d '{"gkey":"test04","info":{"name":"测试组04","pid":1,"items_mrk":"tst04","hirk":"tst04"}}'  http://192.168.10.126:1985/api/reg_group
    #test for reg_items:
    curl -l -H "Content-Type: application/json" -X POST -d '{"gkey":"test01","items":[["测试总数","test.count"],["测试公司","test.corp"]]}'  http://192.168.10.126:1985/api/reg_items
    
    #test fro set:
    curl -l -H "Content-Type: application/json" -X POST -d '{"gkey":"test01","data":{"test.count":[109,0],"test.corp":[50,1448871496]}}'  http://192.168.10.126:1985/api/set
    
    #test for get:
    curl -l -H "Content-Type: application/json" -X POST -d  '{"gkey":"test01","args":{"start_time":1448871496}}'  http://192.168.10.126:1985/api/get
    
 	#test for send:
    curl -l -H "Content-Type: application/json" -X POST -d  '{"gkey":"test01","data":{"test.corp":144496}}'  http://192.168.10.126:1985/api/send
    '''