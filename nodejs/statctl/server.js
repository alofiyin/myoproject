var config= require('./config/main')
var app= require('koa')()

app.name= config.name
app.keys= config.keys
app.env= config.env

app.use(require('koa-bodyparser')(config.bodyparser))
//加载less类css
//app.use(require('koa-less')(config.static.directory))
//加载stylus类css
//app.use(require('koa-stylus')(config.static.directory))

app.use(require('koa-static')(config.static.directory, config.static))

//app.use(require('koa-generic-session')(config.session))
//加载模板
var xtplApp = require('xtpl/lib/koa');
xtplApp(app,{
    views: config.view.root,
    extname:config.view.extname
});
app.use(require('./config/routes')(app));



if (!module.parent) {
	app.listen(config.port || 3000, function(){
		console.log('Server running on port '+config.port || 3000)
	})
} else
	module.exports=app