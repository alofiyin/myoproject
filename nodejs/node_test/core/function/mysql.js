var mysql=require("mysql")
var wrapper = require('co-mysql')
//var  co = require('co');
/*var pool = mysql.createPool({
    host: 'localhost',
    user: 'user',
    password: 'password',
    database: 'database',
    port: 3306
});
*/

/*    	M.base.mysql.query("select * from user_admin where id=?",[90],function(err,res,field){
    		//console.log(err)
    		//console.log(res)
    		_.forEach(res,function(row){
    			_.forEach(row,function(k,v){
    				console.log([v,k])
    				})
    			
    			})
*/
var pool = mysql.createPool(C.sys_mysql)

var p = wrapper(pool);
/*
var query=function *(sql,vals,callback){
	pool.getConnection(function(err,conn){
		if(err){
			callback(err,null,null);
		}else{
			conn.query(sql,vals,function(qerr,res,fields){
				//释放连接
				conn.release();
				//事件驱动回调
				callback(qerr,res,fields);
			});
		}
	});
};

*/
var query = function *(sql,arg){
	var conn = mysql.createConnection(C.sys_mysql)
	var p = wrapper(conn)
	var d = []
	var res = yield p.query(sql,arg)
	conn.end()
	return  res //JSON.parse(JSON.stringify(res))
	}

module.exports={
	query:p.query
	
}

