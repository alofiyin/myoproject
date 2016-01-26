var koa = require('koa');
var app = koa();
var compose  = require('koa-compose');

var load_func = [];
load_func.push(function *(next){
	console.log("step 1.....");
});
load_func.push(function *(next){
	console.log("step 2.....");
});
load_func.push(function *(next){
	console.log("step 3.....");
});

var router = require('koa-router');
var myrouter = new router;

myrouter.all('/i', compose(load_func));
myrouter.all('/t', function *(){
	compose(load_func);
	this.body="just test";});

app.listen(3002);

    app.use(function * pageNotFound(next) {
       //this.body = yield this.render('err/404');
       this.body='404';
       
    });
app.use(myrouter.routes());
    app.on('error', function(err) {
    	
        console.log('server error', err);
    });