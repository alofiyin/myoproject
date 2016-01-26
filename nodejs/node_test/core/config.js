/**
 * Author: ken.xu
 * Date: 14-6-4 下午3:30
 */
module.exports=function(root){
    return {
        //数据库连接
        //mongo:'mongodb://acount:pwd@url:27017/db',
        sys_mysql:{
			    host: '192.168.10.126',
			    user: 'wbsp',
			    password: 'wbsp',
			    database: 'admincenter',
			    port: 3306
			  },
        //系统目录
				controller: root + '/controllers/',
	    	view: {
	        root: root + '/views',
	        extname:'html'
	    	},
	    	default_controller:"index",
	    	default_action:"index",
	    	controller_pre_name:"/",
	    	model: root + '/models/',
        maxAge: 259200000,
        secret:'*&$^*&(*&$%@#@#$@!#$@%((()*()^#$%$#%@#$%@#$%$#',
        //端口设置
	    	name:"后台管理平台",
	    	keys: ['just for test'],
	    	port: 3000,
    }

}