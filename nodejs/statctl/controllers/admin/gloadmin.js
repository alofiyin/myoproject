function *index(next){
		data = {}
		data.title = C.name 
		 data.menu = yield M.mune.m_menu()
		console.log(data)
        yield this.render('admin/index',data)
    }
    
    
function *test(next){
	a = {t:[]}
	b = [1,2,3,4,5,25]
	a[1]="test"
	a[5]="ss"
	a[9]="xx"
	a[2]="xxxx"
	for(k in a){
	console.log(a[k])
}
	}    
module.exports={
	_extend:{ts:function *(next){}},
    index: index,
    test: test,
    login: function *(){
        this.body={success: true}
    }
}