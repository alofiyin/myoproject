function *index(){
	var data={}
	data.weburl=C.weburl;
   	data.defimg=C.weburl+"/css/images/biz72.gif";
   	
        yield this.render('corp/index',data)
    }
    
    
    
module.exports={
	_extend:{ts:function *(next){}},
    index: index,
    login: function *(){
        this.body={success: true}
    }
}