function *index(){
			//console.log(M.base)
    	//console.log(this.params)
    	//console.log(this.request);
    	//console.log(this.request.body)
    	M.base.mysql.query("select * from user_admin where id=?",[90],function(err,res,field){
    		//console.log(err)
    		//console.log(res)
    		_.forEach(res,function(row){
    			_.forEach(row,function(k,v){
    				console.log([v,k])
    				})
    			
    			})
    		//console.log(res)
    		//console.log(field)
    	})
    	data = {a: "just test for zk!",b:"你好，这里是测试内容",abc:'fghght'}
        yield this.render('index/index',data)
    }
    
    
    
module.exports={
	_extend:{ts:function *(next){}},
    index: index,
    login: function *(){
        this.body={success: true}
    }
}