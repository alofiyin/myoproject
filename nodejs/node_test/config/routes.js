var Router= require('koa-router')
var secured = function *(next) {
    if (this.isAuthenticated()) {
        yield next
    } else {
        this.status = 401
    }
}
var fs = require('fs')
var ctl_dict = {}
var reg_ctls = function (){
	fs.readdir(path, callback)
	}
module.exports=function(app){
    var router= new Router();
    ///// Site
    var siteController=require('../controllers/site')
    var zkController=require('../controllers/zk')

    //main
    router.all('/',siteController.index)
    //contact
    router.all('/zk', zkController.index)
    //register
    //router.get('/register', authController.register)
    //router.post('/register', authController.doRegister)


    return router.middleware();
}