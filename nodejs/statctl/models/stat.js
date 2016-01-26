var request = require('koa-request');
var stat_api = function *(fnc,data){ 	
    var opt = {  
        headers: {"Connection": "close"},
        url: C.stat_aip_host+"/api/"+fnc,  
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
var stat_sphinx = function *(data){ 	
    var opt = {  
        headers: {"Connection": "close"},
        url: C.stat_aip_host+"/sphinx/proxy",  
        method: 'POST',
        json:true, 
		body:{param:data}
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
	stat_api:stat_api
}