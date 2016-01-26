var request = require('koa-request');
var zk_api = function *(data){ 	
    var opt = {  
        headers: {"Connection": "close"},
        url: C.stat_aip_host+"/zk",  
        method: 'POST',
        json:true, 
		body:data
    };  	
    var res = yield request(opt);
    var body = res.body
    console.log([res.body])
    if(_.isArray(body) && body[0]===0){
    	return body[1]
    }else
    	
		return []
	
}

module.exports={
	zk_api:zk_api
}