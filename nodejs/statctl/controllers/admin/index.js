function *index(next){
		data = {}
		data.title = C.name 
		 data.menu = yield M.mune.m_menu()
		console.log(data)
        yield this.render('admin/index',data)
    }
    
    
function *test(next){
	console.log(app.router)
}
  
module.exports={
	_extend:{ts:function *(next){}},
    index: index,
    test: test,
    login: function *(){
        this.body={success: true}
    }
}