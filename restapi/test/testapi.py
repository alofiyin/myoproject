#_*_coding:utf-8_*_
from httpwrap import HttpWrap
import json
from pprint import pprint
def curl(mod,act,prama):
	http = HttpWrap()
	http.set_header('Content-Type','application/json')
	body = json.dumps(prama)
	url  = "http://192.168.10.126:6000/%s/%s" % (mod,act)
	res = http.request(url,'POST',body)
	res = json.loads(http.read(res))
	#print(json.dumps(res,indent=1))
	pprint(res)

#加载测试数据文件apidata.py
import apidata
#-----------------
#公司接口bizcom
#-----------------

#插入公司记录cominsert
prama = {}
prama['data']=apidata.com_corp
#curl("bizcom","cominsert",prama)

#更新公司记录comupdate
prama = {}
data = {}
data['id'] = 18944404
data['com_name'] = "测试公司"
prama['data'] = data
#curl("bizcom","comupdate",prama)

#根据id串取公司记录cominfobyid
prama = {}
prama['id'] = '18944390,18944404,18944391'
prama['fields']="id,com_name,con_ddr"
#curl("bizcom","cominfobyid",prama)

#根据公司名取信息cominfobyname
prama = {}
prama['com_name'] = '东莞市兆军电子有限公司'
prama['fields']="id,com_name,con_ddr"
#curl("bizcom","cominfobyname",prama)

#根据公司三级域名获取对应的信息cominfobydomain
prama = {}
prama['domain'] = 'jnjhlkm'
#prama['fields']="id,com_name,con_ddr"
#curl("bizcom","cominfobydomain",prama)

#根据用户id获取公司的信息(单条信息)cominfobyuseridone
#根据用户id获取公司的信息(多条信息)cominfobyuserid
prama = {}
prama['userid'] = '1059236'
#prama['fields']="id,com_name,con_ddr"
#curl("bizcom","cominfobyuseriddone",prama)

#删除公司comdelete
prama = {}
prama['id']=18944404
#curl("bizcom","comdelete",prama)


#插入公司审核记录checkinsert
prama = {}
prama['data']=apidata.com_corp
#curl("bizcom","checkinsert",prama)

#更新公司审核记录checkupdate
prama = {}
data = {}
data['id'] = 18943760
data['com_name'] = "测试公司"
prama['data'] = data
#curl("bizcom","checkupdate",prama)

#删除公司checkdelete
prama = {}
prama['id']=18943760
#curl("bizcom","checkdelete",prama)

#取审核记录
prama = {}
#curl("bizcom","checklist",prama)

#取审核记录条数
prama = {}
#prama['page']=18943760
#curl("bizcom","checkcount",prama)

#插入公司标签关联值taginsert
prama = {}
prama['data']={'com_id':8602410,'tag_id':113162107}
#curl("bizcom","taginsert",prama)
#更新公司标签关联值tagupdate
prama = {}
data = {}
data['id'] = 27164962
data['tag_id'] = 113162106
prama['data'] = data
#curl("bizcom","tagupdate",prama)
#删除公司标签关联值tagdelete
prama = {}
prama['id']=27164962
#curl("bizcom","tagdelete",prama)
#根据id获取一条公司标签关联值
prama = {}
prama['id']=23036976
#curl("bizcom","taginfobyid",prama)
#根据公司id获取一条公司标签关联值
prama = {}
prama['comid']=8662451
#curl("bizcom","taginfobycomid",prama)

#插入公司标签关联值taginsert
prama = {}
prama['data']={'com_id':8602410,'keyw':"测试"}
#curl("bizcom","keywinsert",prama)
#更新公司标签关联值tagupdate
prama = {}
data = {}
data['id'] = 1179396
data['keyw'] = '测试111'
prama['data'] = data
#curl("bizcom","keywupdate",prama)
#删除公司展厅关键字tagdelete
prama = {}
prama['id']=1179396
#curl("bizcom","keywdelete",prama)
#根据id获取一条公司展厅关键字
prama = {}
prama['id']=170
#curl("bizcom","keywinfobyid",prama)
#根据公司id获取一条公司展厅关键字
prama = {}
prama['comid']=10564220
#curl("bizcom","keywinfobycomid",prama)


#插入公司相册类
prama = {}
prama['data']={'com_id':262357,'name':"测试"}
#curl("bizcom","albuminsert",prama)
#更新公司相册类
prama = {}
data = {}
data['id'] = 29446
data['name'] = '测试111'
prama['data'] = data
#curl("bizcom","albumupdate",prama)
#删除公司相册类
prama = {}
prama['id']=29446
#curl("bizcom","albumdelete",prama)
#根据id获取一条公司相册类
prama = {}
prama['id']=117
#curl("bizcom","albuminfobyid",prama)
#根据公司公司相册-分页
prama = {}
prama['pageSize'] = 2
prama['page'] = 2
prama['comid']=262357
#curl("bizcom","albumlistbycomid",prama)
#取公司相册记录条数
prama = {}
prama['comid']=262357
#curl("bizcom","albumcount",prama)

#插入公司相册图片
prama = {}
prama['data']={'com_id':260973,'title':"测试"}
#curl("bizcom","photosinsert",prama)
#更新公司相册图片
prama = {}
data = {}
data['id'] = 162104
data['title'] = '测试111'
prama['data'] = data
#curl("bizcom","photosupdate",prama)
#删除公司相册图片
prama = {}
prama['id']=162104
#curl("bizcom","photosdelete",prama)
#根据id获取一条公司相册图片
prama = {}
prama['id']=13360
#curl("bizcom","photosinfobyid",prama)
#根据公司相册图片-分页
prama = {}
prama['pageSize'] = 2
prama['page'] = 2
prama['comid']=260973
prama['albumid']=172
#curl("bizcom","photoslistbycomid",prama)
#取公司相册图片记录条数
prama = {}
prama['comid']=260973
prama['albumid']=172
#curl("bizcom","photoscount",prama)

#插入公司友情链接
prama = {}
prama['data']={'com_id':260973,'title':"测试"}
#curl("bizcom","friendinsert",prama)
#更新公司友情链接
prama = {}
data = {}
data['id'] = 19269
data['title'] = '测试111'
prama['data'] = data
#curl("bizcom","friendupdate",prama)
#删除公司友情链接
prama = {}
prama['id']=19270
#curl("bizcom","frienddelete",prama)
#根据id获取一条公司友情链接
prama = {}
prama['id']=18
#curl("bizcom","friendinfobyid",prama)
#根据公司友情链接-分页
prama = {}
prama['pageSize'] = 2
prama['page'] = 2
prama['comid']=12212832
#curl("bizcom","friendlistbycomid",prama)
#取公司友情链接记录条数
prama = {}
prama['comid']=260973
#curl("bizcom","friendcount",prama)

#插入公司动态
prama = {}
prama['data']={'com_id':260973,'title':"测试"}
#curl("bizcom","newsinsert",prama)
#更新公司动态
prama = {}
data = {}
data['id'] = 1165161
data['title'] = '测试111'
prama['data'] = data
#curl("bizcom","newsupdate",prama)
#删除公司动态
prama = {}
prama['id']=1165161
#curl("bizcom","newsdelete",prama)
#根据id获取一条公司动态
prama = {}
prama['id']=260973
#curl("bizcom","newsinfobyid",prama)
#根据公司动态-分页
prama = {}
prama['pageSize'] = 2
prama['page'] = 2
prama['comid']=260973
prama['where'] = "status=1"
#curl("bizcom","newslistbycomid",prama)
#取公司动态记录条数
prama = {}
prama['comid']=260973
#curl("bizcom","newscount",prama)

#插入公司证书
prama = {}
prama['data']={'com_id':260973,'name':"测试"}
#curl("bizcom","certinsert",prama)
#更新公司证书
prama = {}
data = {}
data['id'] = 85082
data['name'] = '测试111'
prama['data'] = data
#curl("bizcom","certupdate",prama)
#删除公司证书
prama = {}
prama['id']=85082
#curl("bizcom","certdelete",prama)
#根据id获取一条公司证书
prama = {}
prama['id']=4430
#curl("bizcom","certinfobyid",prama)
#根据公司证书-分页
prama = {}
prama['pageSize'] = 2
prama['page'] = 1
prama['comid']=8550392
#prama['where'] = "status=1"
#curl("bizcom","certlistbycomid",prama)
#取公司证书记录条数
prama = {}
prama['comid']=8550392
#curl("bizcom","certcount",prama)

#插入公司黑名单
prama = {}
prama['data']={'com_id':260973,'com_name':"测试"}
#curl("bizcom","blackinsert",prama)
#更新公司黑名单
prama = {}
data = {}
data['id'] = 666
data['com_name'] = '测试111'
prama['data'] = data
#curl("bizcom","blackupdate",prama)
#删除公司黑名单
prama = {}
prama['id']=666
#curl("bizcom","blackdelete",prama)
#根据id获取一条公司黑名单
prama = {}
prama['id']=20
#curl("bizcom","blackinfobyid",prama)
#根据公司黑名单-分页
prama = {}
prama['pageSize'] = 2
prama['page'] = 1
#prama['where'] = "status=1"
#curl("bizcom","blacklist",prama)
#取公司黑名单记录条数
prama = {}
prama['comid']=12307903
#curl("bizcom","blackcount",prama)

#插入公司违法记录
prama = {}
prama['data']={'com_id':260973,'com_name':"测试"}
#curl("bizcom","illegalinsert",prama)
#更新公司违法记录
prama = {}
data = {}
data['id'] = 1794
data['com_name'] = '测试111'
prama['data'] = data
#curl("bizcom","illegalupdate",prama)
#删除公司违法记录
prama = {}
prama['id']=1794
curl("bizcom","illegaldelete",prama)
#根据id获取一条公司违法记录
prama = {}
prama['id']=1789
#curl("bizcom","illegalinfobyid",prama)
#根据公司违法记录-分页
prama = {}
prama['pageSize'] = 2
prama['page'] = 1
#prama['where'] = "status=1"
#curl("bizcom","illegallist",prama)
#取公司违法记录记录条数
prama = {}
prama['where']='com_id=16334596'
#curl("bizcom","illegalcount",prama)

#插入公司设置
prama = {}
prama['data']={'com_id':260973,'item_key':"template","item_value":"top88,0","item":"bg"}
#curl("bizcom","settinginsert",prama)
#更新公司设置
prama = {}
data = {}
data['id'] = 11399873
data['item_value'] = 'top87,0'
prama['data'] = data
#curl("bizcom","settingupdate",prama)
#删除公司设置
prama = {}
prama['id']=11399873
#curl("bizcom","settingdelete",prama)
#根据id获取一条公司设置
prama = {}
prama['id']=8979478
#curl("bizcom","settinginfobyid",prama)
#根据公司设置-分页
prama = {}
prama['pageSize'] = 2
prama['page'] = 1
prama['comid'] = "16533041"
#curl("bizcom","settinglistbycomid",prama)
#取公司设置记录条数
prama = {}
prama['comid']=12943924
#curl("bizcom","settingcount",prama)

#插入公司模版
prama = {}
prama['data']={'title':"测试"}
#curl("bizcom","tplinsert",prama)
#更新公司模版
prama = {}
data = {}
data['id'] = 29
data['title'] = '测试11'
prama['data'] = data
#curl("bizcom","tplupdate",prama)
#删除公司模版
prama = {}
prama['id']=29
#curl("bizcom","tpldelete",prama)
#根据id获取一条公司模版
prama = {}
prama['id']=19
#curl("bizcom","tplinfobyid",prama)
#根据公司模版-分页
prama = {}
prama['pageSize'] = 2
prama['page'] = 1
prama['where'] = "title='交通运输'"
#curl("bizcom","tpllist",prama)
#取公司模版记录条数
prama = {}
prama['where']="title='交通运输'"
#curl("bizcom","tplcount",prama)

#插入公司模版标签
prama = {}
prama['data']={'title':"测试"}
#curl("bizcom","tpltaginsert",prama)
#更新公司模版标签
prama = {}
data = {}
data['id'] = 29
data['title'] = '测试11'
prama['data'] = data
curl("bizcom","tpltagupdate",prama)
#删除公司模版标签
prama = {}
prama['id']=29
curl("bizcom","tpltagdelete",prama)
#根据id获取一条公司模版标签
prama = {}
prama['id']=19
#curl("bizcom","tpltaginfobyid",prama)
#根据公司模版标签-分页
prama = {}
prama['pageSize'] = 2
prama['page'] = 1
prama['where'] = "title='交通运输'"
#curl("bizcom","tptagllistbycomid",prama)
#取公司模版标签记录条数
prama = {}
prama['where']="title='交通运输'"
#curl("bizcom","tplcount",prama)