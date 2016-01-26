function *index(){
	var data={}
	data.weburl=C.weburl;
   	data.defimg=C.weburl+"/css/images/biz72.gif";
	//获取标签
   	var prama = {biznum:"com.corp_targ"}
   	var func = "gettags"
	var tag_dict = yield M.stat.biz_tags(func,prama)
	data.tag_arr=tag_dict.extn
	//公司列表
	prama = {biznum:"com.corp_list"}
	//var com_list = yield M.stat.biz_tags(func,prama)
	//字母表
	data.larr=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
   	data.title = "公司黄页-公司库,公司黄页,企业名录,供应商大全-商务联盟"
        yield this.render('corp/index',data)
    }
    
    
    
module.exports={
	_extend:{ts:function *(next){}},
    index: index,
    login: function *(){
        this.body={success: true}
    }
}