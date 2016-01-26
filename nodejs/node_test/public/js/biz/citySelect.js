
/**
通用的省市联动JS
使用方法：
初始化：_MyMVC_citySelect.init(pId,cId,def)
pId:省的下拉菜单ID
cId:市的下拉菜单ID 
def:为默认的已先择值 可选
def[0] 省的默认值 
def[1] 市的默认值 
例：
_MyMVC_citySelect.init("province","city",["吉林","白山"]);
_MyMVC_citySelect.init("province","city",["吉林"]);
_MyMVC_citySelect.init("province","city",[]);
_MyMVC_citySelect.init("province","city",["吉林","白山"],["省份","城市"]);

重置为默认状态：
_MyMVC_citySelect.reset();

 一个页面中有多个时：
var citySelect01=new _My_citySelect();
citySelect01.init("province","city",["",""],["省份","城市"]);

 
var citySelect02=new _My_citySelect();
citySelect02.init("province2","city2",["",""],["省份","城市"]);
*/
function   _My_citySelect()
{
	this.pc=[];
	this.def=[];
	this.p=null;
	this.c=null;
	this.cId=null;
	this.isTips=true;
	this.initStart=0;
	this.init=function (pId,cId,def,optDef)
	{
		var optsDef = optDef || ["请选择省份名","请选择城市名"];
		if (this.isTips) 
		{
			this.pc[0]= new Array(optsDef[0],"|"+optsDef[1]);
		}
		else
		{
			this.initStart=1;	
		}
		this.cId=cId;

		this.pc[1] = new Array("北京","|北京");
		this.pc[2] = new Array("天津","|天津");
		this.pc[3] = new Array("上海","|上海");
		this.pc[4] = new Array("重庆","|重庆");
		this.pc[5] = new Array("河北","|石家庄|唐山|秦皇岛|邯郸|邢台|保定|张家口|承德|沧州|廊坊|衡水");
		this.pc[6] = new Array("山西","|太原|大同|阳泉|长治|晋城|朔州|晋中|运城|忻州|临汾|吕梁");
		this.pc[7] = new Array("河南","|郑州|开封|洛阳|平顶山|安阳|鹤壁|新乡|焦作|濮阳|许昌|漯河|三门峡|南阳|商丘|信阳|周口|驻马店|济源");
		this.pc[8] = new Array("辽宁","|沈阳|大连|鞍山|抚顺|本溪|丹东|锦州|营口|阜新|辽阳|盘锦|铁岭|朝阳|葫芦岛");
		this.pc[9] = new Array("吉林","|长春|吉林|四平|辽源|通化|白山|松原|白城|延边朝鲜族自治州");
		this.pc[10] = new Array("黑龙江","|哈尔滨|齐齐哈尔|鸡西|鹤岗|双鸭山|大庆|伊春|佳木斯|七台河|牡丹江|黑河|绥化|大兴安岭");
		this.pc[11] = new Array("内蒙古","|呼和浩特|包头|乌海|赤峰|通辽|鄂尔多斯|呼伦贝尔|巴彦淖尔|乌兰察布|兴安盟|锡林郭勒盟|阿拉善盟");
		this.pc[12] = new Array("江苏","|南京|无锡|徐州|常州|苏州|南通|连云港|淮安|盐城|扬州|镇江|泰州|宿迁");
		this.pc[13] = new Array("山东","|济南|青岛|淄博|枣庄|东营|烟台|潍坊|济宁|泰安|威海|日照|莱芜|临沂|德州|聊城|滨州|菏泽");
		this.pc[14] = new Array("安徽","|合肥|芜湖|蚌埠|淮南|马鞍山|淮北|铜陵|安庆|黄山|滁州|阜阳|宿州|巢湖|六安|亳州|池州|宣城");
		this.pc[15] = new Array("浙江","|杭州|宁波|温州|嘉兴|湖州|绍兴|金华|衢州|舟山|台州|丽水");
		this.pc[16] = new Array("福建","|福州|厦门|莆田|三明|泉州|漳州|南平|龙岩|宁德");
		this.pc[17] = new Array("湖北","|武汉|黄石|十堰|宜昌|襄阳|鄂州|荆门|潜江|天门|仙桃|孝感|荆州|黄冈|咸宁|随州|恩施土家族苗族自治州|神农架林区");
		this.pc[18] = new Array("湖南","|长沙|株洲|湘潭|衡阳|邵阳|岳阳|常德|张家界|益阳|郴州|永州|怀化|娄底|湘西土家族苗族自治州");
		this.pc[19] = new Array("广东","|广州|韶关|深圳|珠海|汕头|佛山|江门|湛江|茂名|肇庆|惠州|梅州|汕尾|河源|阳江|清远|东莞|中山|潮州|揭阳|云浮");
		this.pc[20] = new Array("广西","|南宁|柳州|桂林|梧州|北海|防城港|钦州|贵港|玉林|百色|贺州|河池|来宾|崇左");
		this.pc[21] = new Array("江西","|南昌|景德镇|萍乡|九江|新余|鹰潭|赣州|吉安|宜春|抚州|上饶");
		this.pc[22] = new Array("四川","|成都|自贡|攀枝花|泸州|德阳|绵阳|广元|遂宁|内江|乐山|南充|眉山|宜宾|广安|达州|雅安|巴中|资阳|阿坝藏族羌族自治州|甘孜藏族自治州|凉山彝族自治州");
		this.pc[23] = new Array("贵州","|贵阳|六盘水|遵义|安顺|铜仁|黔西南布依族苗族自治州|毕节|黔东南苗族侗族自治州|黔南布依族苗族自治州");
		this.pc[24] = new Array("云南","|昆明|曲靖|玉溪|保山|昭通|丽江|普洱|临沧|楚雄彝族自治州|红河哈尼族彝族自治州|文山壮族苗族自治州|西双版纳傣族自治州|大理白族自治州|德宏傣族景颇族自治州|怒江傈傈族自治州|迪庆藏族自治州");
		this.pc[25] = new Array("西藏","|拉萨|昌都|山南|日喀则|那曲|阿里|林芝");
		this.pc[26] = new Array("海南","|海口|三亚|琼海|东方|儋州|万宁|文昌|定安县|五指山|屯昌县|澄迈县|临高县|白沙黎族自治县|昌江黎族自治县|乐东黎族自治县|陵水黎族自治县|琼中黎族苗族自治县|保亭黎族苗族自治县|西沙群岛|南沙群岛|中沙群岛的岛礁及其海域");
		this.pc[27] = new Array("陕西","|西安|铜川|宝鸡|咸阳|渭南|延安|汉中|榆林|安康|商洛");
		this.pc[28] = new Array("甘肃","|兰州|嘉峪关|白银|天水|武威|张掖|平凉|酒泉|庆阳|定西|陇南|金昌|临夏回族自治州|甘南藏族自治州");
		this.pc[29] = new Array("宁夏","|银川|石嘴山|吴忠|固原|中卫");
		this.pc[30] = new Array("青海","|西宁|海东|海北藏族自治州|黄南藏族自治州|海南藏族自治州|果洛藏族自治州|玉树藏族自治州|海西蒙古族藏族自治州");
		this.pc[31] = new Array("新疆","|乌鲁木齐|克拉玛依|吐鲁番|哈密|昌吉回族自治州|博尔塔拉蒙古自治州|巴音郭楞蒙古自治州|阿克苏|克孜勒苏柯尔克孜自治州|喀什|和田|伊犁哈萨克自治州|塔城地区|阿勒泰地区|阿拉尔|石河子|五家渠|图木舒克");
		this.pc[32] = new Array("香港","|香港岛|九龙|新界");
		this.pc[33] = new Array("澳门","|澳门半岛|澳门离岛");
		this.pc[34] = new Array("台湾","|台北县|宜兰县|桃园县|新竹县|苗栗县|台中县|彰化县|南投县|云林县|嘉义县|台南县|高雄县|屏东县|台东县|花莲县|澎湖县|基隆市|新竹市|台中市|嘉义市|台南市|台北市|高雄市|金门县|连江县");

		//----------------------------------------------------
		this.p = this.$(pId);
		this.c = this.$(cId);
		def=def || {};
		def[0]= def[0] || false;
		def[1]= def[1] || false;
		def[2]=false;
		this.def=def;
		this.initSelect();
		//----------------------------------------------------
	}
	//------------------------------------------------------
	this.reset=function ()
	{
		this.def[2]=false;
		this.def[3].selected=true; 
		this.showcity(this.def[4]);
	}
	//------------------------------------------------------
	this.initSelect=function ()
	{
		if (this.p) 
		{
		   var me=this;
		   var defIdx=this.initStart;
		   for( var i = this.initStart; i < this.pc.length; i++ ) 
		   {
				e = document.createElement( "option" );
				e.setAttribute( "value", this.pc[i][0] );
				e.setAttribute( "cp_idx", i );
				if (me.def[0]==this.pc[i][0])
				{
					e.setAttribute( "selected",true); 
					defIdx=i;
					me.def[3]=e;
					me.def[4]=defIdx;
				}
				e.innerHTML = this.pc[i][0];				
				var tmp=i;
				this.p.onchange=function ()
				{
					var idx=this.options[this.selectedIndex].getAttribute("cp_idx");
					//alert(this.id);
					me.showcity(idx);
				}
				this.p.appendChild(e);
		   }
		   this.showcity(defIdx);
		}
		else
		{
			alert("你的省分下拉菜单对象无法获取，可能是ID错误。");
		}
	}
	//------------------------------------------------------
	this.showcity=function (idx) 
	{
		var c = this.c;
		//alert(c.id);
		if (c) {while(c.hasChildNodes()){c.removeChild(c.lastChild);}}
		else
		{
			alert("你的城市下拉菜单对象无法获取，可能是ID错误。");
		}
		var citys = this.pc[idx][1].split( "|" ); 	
		//alert(citys);
		for( var i = 1; i < citys.length; i++ ) 
		{
			e = document.createElement( "option" );
			e.setAttribute( "value", citys[i] );
			if (this.def[1]==citys[i] && this.def[2]==false)
			{
				e.setAttribute( "selected",true); 
				this.def[2]==true;
			}
			e.innerHTML = citys[i];
			c.appendChild(e);
		}
	}
	//------------------------------------------------------
	this.$=function (id){return document.getElementById(id);}
}
//默认的全局实例
var _MyMVC_citySelect=new _My_citySelect ();