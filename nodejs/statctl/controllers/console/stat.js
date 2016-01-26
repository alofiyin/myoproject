function *index(next){
	/*统计组列表*/
		data = {};
		grid = {};
		grid.title = "统计组列表";
		grid.dataid = "stat_group";
		grid.opt = {url:"/console/stat/groupdata",method:"get"}
		filelds =[
        	{field:'ck',checkbox:1},
        		{field:'name',title:'名称',editor:'textbox',},
        		{field:'gkey',title:'键名',align:'right',editor:'textbox'},
        		{field:'pid',title:'pid',align:'right',editor:'textbox'},
        		{field:'items_mrk',title:'items_mrk',align:'right',editor:'textbox'},
        		{field:'history_mr',title:'history_mr',align:'right',editor:'textbox'},
        		{field:'sumdelay',title:'统计时间',align:'right',editor:'textbox'}
    		];
		//grid.fields = JSON.stringify(filelds);
		grid.fields = filelds;
		//grid.menu = yield M.mune.m_menu();
		data.grid=grid
        yield this.render('gload/datagrid2',data);
        //yield this.render('gload/test',data);
    }

function *item(next){
	/*统计项列表*/
		data = {};
		grid = {};
		grid.title = "统计项列表";
		grid.dataid = "stat_item";
		grid.opt = {url:"/console/stat/itemdata",method:"post"}
		filelds =[
        		{field:'name',title:'名称',width:'30%'},
        		{field:'itemkey',title:'键名',width:'30%'},

    		];
		//grid.fields = JSON.stringify(filelds);
		grid.fields = filelds;
		//grid.menu = yield M.mune.m_menu();
		data.grid=grid
    	var d  = {"gkeys":"all"};
    	groups =  yield M.stat.stat_api("get_groups",d);
    	data.groups = groups
        yield this.render('stat/item',data);
        //yield this.render('gload/test',data);
		
}

function *history(next){
	/*统计数据列表*/
	var data = {};
	var grid = {};
	grid.title = "统计数据列表";
	grid.dataid = "stra_history";
	grid.opt = {url:"/console/stat/historydata",method:"post"}
	var filelds =[
        		{field:'name',title:'名称',width:'30%'},
        		{field:'clock',title:'统计时间',align:'right',width:'30%'},
        		{field:'val',title:'val',align:'right',width:'30%'},

    		];	
    grid.fields = filelds;
    data.grid=grid
    var d  = {"gkeys":"all"};
    groups =  yield M.stat.stat_api("get_groups",d);
    data.groups = groups
    yield this.render('stat/histor',data);		
}   

function *search(next){
	/*实时统计查询*/
	var data = {}
	yield this.render('stat/search',data);	
}

function *historydata(next){
	/*获取统计数据*/
		var data = this.request.body;
		var res = yield M.stat.stat_api("get",data);
		console.log(res)
		var body = []
		for( i in res[1]){
			res[1][i].name=res[0][res[1][i].itemid]
			res[1][i].clock=M.base.date.format(res[1][i].clock,'yyyy-mm-dd hh:ii:ss')
		}
		yield next
		this.body=res[1];
} 
function *groupdata(next){
	/*获取统计组数据*/
	var data = this.request.body;
	var data  = {"gkey":"all"};	
    res = yield M.stat.stat_api("get_groups",data);

	yield next 
	this.body=res;

	
}  
	
function *itemdata(next){
	/*获取统计项数据*/
	var data = this.request.body;
    res = yield M.stat.stat_api("get_items",data);
	console.log(res)
	yield next 
	this.body=res;
}	  
function *test(next){
	yield next;
	this.body='{[{"productid":"FI-SW-01","productname":"Koi","unitcost":10.00,"status":"P","listprice":36.50,attr1":"Large","itemid":"EST-1"},{"productid":"K9-DL-01","productname":"Dalmation","unitcost":12.00,"status":"P","listprice":18.50,"attr1":"Spotted Adult Female","itemid":"EST-10"},{"productid":"RP-SN-01","productname":"Rattlesnake","unitcost":12.00,"status":"P","listprice":38.50,"attr1":"Venomless","itemid":"EST-11"},{"productid":"RP-SN-01","productname":"Rattlesnake","unitcost":12.00,"status":"P","listprice":26.50,"attr1":"Rattleless","itemid":"EST-12"},{"productid":"RP-LI-02","productname":"Iguana","unitcost":12.00,"status":"P","listprice":35.50,"attr1":"Green Adult","itemid":"EST-13"},{"productid":"FL-DSH-01","productname":"Manx","unitcost":12.00,"status":"P","listprice":158.50,"attr1":"Tailless","itemid":"EST-14"},{"productid":"FL-DSH-01","productname":"Manx","unitcost":12.00,"status":"P","listprice":83.50,"attr1":"With tail","itemid":"EST-15"},{"productid":"FL-DLH-02","productname":"Persian","unitcost":12.00,"status":"P","listprice":23.50,"attr1":"Adult Female","itemid":"EST-16"},{"productid":"FL-DLH-02","productname":"Persian","unitcost":12.00,"status":"P","listprice":89.50,"attr1":"Adult Male","itemid":"EST-17"},{"productid":"AV-CB-01","productname":"Amazon Parrot","unitcost":92.00,"status":"P","listprice":63.50,"attr1":"Adult Male","itemid":"EST-18"}]}'

}
  
module.exports={
	_extend:{ts:function *(next){}},
    group: index,
    t: test,
	groupdata:groupdata,
	history,history,
	historydata,historydata,
	item,item,
	itemdata,itemdata,
	search,search
	
	
}