var sql = "select * from user_admin_menu where pid=? and is_show=1"
var m_menu = function *(){
		var menu ={menus:[]}
		var sql = "select * from user_admin_menu where pid=0 and is_show=1"
		var res = yield M.base.mysql.query(sql)
		for(k in res){
			if(res[k]){
			var submenu={}
			submenu.menuid = res[k].id
			submenu.menuname = res[k].name
			tmp = yield treemenu(res[k].id)
			submenu.menus=JSON.parse(tmp)
	
			menu.menus.push(submenu)
		}
		}
		return JSON.stringify(menu)
}

var treemenu = function *(pid){
		var menu =[]
		var res = yield M.base.mysql.query(sql,[pid])
		for(k in res){

			if(res[k]){

			var submenu={}
			submenu.id = res[k].id
			submenu.text = res[k].name
			submenu.state="closed"
			submenu.children = []
			var rs = yield M.base.mysql.query(sql,[res[k].id])
			for(j in rs){
				tmp = {}
				tmp.id = rs[j].id
				
				var url = '/'
				if(rs[j].module)
					url+=rs[j].module+'/'
				if(rs[j].file_name)
					url+=rs[j].file_name+'/'
				if(rs[j].action_name)
					url+=rs[j].action_name+'/'
				tmp.text = '<a target="mainFrame" href="' + url + '" >' + rs[j].name + '</a>'
				submenu.children.push(tmp)
			}
			
			menu.push(submenu)
		}
		}
	return JSON.stringify(menu)

}

var leftmenu = function *(pid,next){
		var menu ={menus:[]}
		var res = yield M.base.mysql.query(sql,[pid])
		console.log('11111',res)
		for(k in res){
			console.log(res[k])
			if(res[k]){

			var submenu={}
			submenu.menuid = res[k].id
			submenu.menuname = res[k].name
			submenu.menus = []
			var rs = yield M.base.mysql.query(sql,[res[k].id])
			for(j in rs){
				tmp = {}
				tmp.menuid = rs[j].id
				tmp.menuname = rs[j].name
				tmp.url = '/'
				if(rs[j].module)
					tmp.url+=rs[j].module+'/'
				if(rs[j].file_name)
					tmp.url+=rs[j].file_name+'/'
				if(rs[j].action_name)
					tmp.url+=rs[j].action_name+'/'
				submenu.menus.push(tmp)
			}
			menu.menus.push(submenu)
		}
		}

	return JSON.stringify(menu)
}
    
function topmenu(){
		menu = {} 
		M.base.mysql.query(sql,[],function(err,res,f){
			_.forEach(res,function(row){
				var pid = row.id
				menu.pid = 0
				})
			})
		return menu	
	}    
    
module.exports={
	leftmenu:leftmenu,
	treemenu:treemenu,
	m_menu:m_menu
}