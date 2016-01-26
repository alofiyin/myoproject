function *index(next){
		data = {}
		data.title = C.name 
		 data.menu = yield M.mune.m_menu()
		console.log(data)
        yield this.render('gload/treegrid',data)
    }
    
    
function *get_children(next){
	pt = this.request.body['path']
	var data  = {"cmd":"get_children",'args':[pt]};	
    res = yield M.zk.zk_api(data);

	yield next 
	this.body=res;

}
  
module.exports={
	_extend:{ts:function *(next){}},
    index: index,
    test: get_children,
    login: function *(){
        this.body={success: true}
    }
}