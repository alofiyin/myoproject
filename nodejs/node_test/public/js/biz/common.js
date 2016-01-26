//-----------------------------------------------------------------------
/*
*****************************
yxh0612@163.com js_lib * HTML相关函式库
Lastdate：2006-07-27 22:58
QQ：3906261(夜之子,飞飞)
Copyright：Doublefly 叶雄辉
*****************************
*/
//-----------------------------------------------------------------------

//通用的JS库  配置
var _MyMVC_INI={};
//可选值0非调试状态 1 普通调试状态，友好提示 2 管理员调试
_MyMVC_INI.isDebugMod	=0;
_MyMVC_INI.debugPanel	="_MyMVC_debug_panel";
_MyMVC_INI.noMenu		=false;//是否禁止浏览器的右键
_MyMVC_INI.noSelect		=false;//是否禁止浏览器选择
//-----------------------------------------------------------------------
var FBrowser=new Object();
FBrowser.isIE=((navigator.userAgent.indexOf('MSIE')==-1)?false:true);
FBrowser.isIE7=((FBrowser.isIE&&window.XMLHttpRequest)?true:false);
FBrowser.isIE6=((FBrowser.isIE&&!window.XMLHttpRequest&&window.ActiveXObject)?true:false);
FBrowser.isFirefox=((navigator.userAgent.indexOf('Firefox')==-1)?false:true);
FBrowser.isOpera=((navigator.userAgent.indexOf('Opera')==-1)?false:true);
String.prototype.lTrim=function(){return this.replace(/^\s*/,"");}
String.prototype.rTrim=function(){return this.replace(/\s*$/,"");}
String.prototype.trim=function(){return this.rTrim().lTrim();}
String.prototype.hasChinese=function(){return/[^\x00-\xff]/g.test(this);}
Array.prototype.exist=function(v)
{
	var c=this.length;
	for(var i=0;i<c;i++){if(this[i]==v)return true;}
	return false;
}
window.clearRunInterval=window.clearInterval;
window.clearRunTimeout=window.clearTimeout;
window.setRunTimeout=function(fn,dt)
{
	if(typeof(fn)!='function')return false;
	var p=new Array();
	var c=arguments.length;
	if(c>2){for(var i=2;i<c;i++)p[i-2]=arguments[i];}
	var f=function(){fn.apply(null,p)}
	return window.setTimeout(f,dt);
}
window.setRunInterval=function(fn,dt)
{
	if(typeof(fn)!='function')return false;
	var p=new Array();
	var c=arguments.length;
	if(c>2){for(var i=2;i<c;i++)p[i-2]=arguments[i];}
	var f=function(){fn.apply(null,p)}
	return window.setInterval(f,dt);
}
function Fid(id){return document.getElementById(id);}
function Fname(name){return document.getElementsByName(name);}
function FtagName(name){return document.getElementsByTagName(name);}
function Fempty(v){return((""==v||undefined==v||null==v)?true:false);}
function DelFormID(id){return Fid(id).parentNode.removeChild(Fid(id));}
function FgetObjPos(id)
{
	var e=Fid(id);
	var a=new Array()
	var t=e.offsetTop;
	var l=e.offsetLeft;
	var w=e.offsetWidth;
	var h=e.offsetHeight;
	while(e=e.offsetParent)
	{
		 t+=e.offsetTop;
		 l+=e.offsetLeft;
	}
	return {l:l,t:t,w:w,h:h};
}
//-----------------------------------------------------------------------
/*
_MyMVC_ajax 使用说明：

一：_MyMVC_ajax 的请求处理选项
	0. 请法处理选项为一个对象 如：opt={}
	1. opt.handlerAgent 
		是用于设置 _MyMVC_ajax 数据请求内核的参数，可选值为：IFM,XMLHTTP
		_MyMVC_ajax 内置了两种数据请求提交内核
		一个是基于XMLHTTP的
		一种是基于DHTM的，用隐藏IFRAME实现
		注：只有当需要使用 _MyMVC_ajax 提交上传图片的表单时必须使用 IFM
			非上传图片时，强烈建议使用XMLHTTP内核
			当 opt.handlerAgent=XMLHTTP 不能上传图片
			此外，当 opt.handlerAgent=IFM 时，opt.async 是无效的，始终于异步方式提交
	
	2. opt.queryH 
		是用于提交的GET或者POST数据 是 k->v 形式的HASH对象
		如：opt.queryH={test:"a中国--post--在aa",aaab:"你好吗？"};
		或：opt.queryH.testP="testV";
		在服务端可用 $_GET["test"] $_GET["testP"] $_GET["aaab"] 或者 $_GET[key] 取得值
		注：_MyMVC_ajax 的数据统一使用UTF-8编码提交，默认为空
		
	3. opt.callBack
		是用于AJAX的数据回调处理JS函数，非字符串
		如：opt.callBack=alert，会将服务器返回的数据 alert 出来
		注：函数的参数为回调返回的内容，默认为空即对返回内容不作处理
		
	4. opt.insertId	 
		是用于显示服务器返回内容的DHTML容器ID，如：某DIV的ID
		注：如果设置则将结果更新到目标容器 默认为null
	
	5. opt.method	 
		数据提交方式可选值为： GET 或者 POST 
		注：GET 的方式只能处理数参图短的情况（URL的长度限制）
			如果要提交表单，强烈建议使用POST方式(不能用于上传图片)，默认为GET
			
	6. opt.async	 
		数据是否以异步的方式提交，默认为 TRUE
		注：当 opt.handlerAgent=IFM 时，无效，始终于异步方式提交
	
	7. opt.loading	 
		当正在服务端执行时客户端的处理对象，它包括两个方法 start , end 
		当 _MyMVC_ajax 向服务器提交数据时 执行，opt.loading.start();
		当 _MyMVC_ajax 处理完成时 执行，opt.loading.end();
		如：opt.loading={start:function(){},end:function (){}}; 默认
		
二：_MyMVC_ajax 的调用方法
	所有调用方法中
	opt		为请求处理选项，使用说明同上
	url		为请求目标地址 可以包含查询值，如：index.php?act=test
	formId  为当需要用_MyMVC_ajax提交表单时的表单ID，必须唯一
	module	为MyMVC专用调用方法的参数，规则即为MyMVC的模块规则
	
	通用调用方法：
	1.  以 opt 为请求选项，提交给 url 处理
		_MyMVC_ajax.get(url,opt);
	2. 以 opt 为请求选项，将ID为 formId 的表单提交给 url 处理
		_MyMVC_ajax.formPost(formId,url,opt);
		
	MyMVC专用调用方法：	
	3. 以 opt 为请求选项，提交给 应用模块：module 处理
		_MyMVC_ajax.appGet(module,opt);
	
	4. 以 opt 为请求选项，将ID为 formId 的表单提交给 应用模块：module 处理
		_MyMVC_ajax.appForm(formId,module,opt);
		
	3. 以 opt 为请求选项，提交给 系统模块：module 处理
		_MyMVC_ajax.mvcGet(module,opt);
	
	4. 以 opt 为请求选项，将ID为 formId 的表单提交给 系统模块：module 处理
		_MyMVC_ajax.mvcForm(formId,module,opt);
	
二：_MyMVC_ajax 的调用实例
	使用前请确定你已经加载 _MyMVC_ajax 包文件	
	function test1()
	{
		var url = 'http://192.168.1.101:8001/_mymvc/test.php';
		var opt={};
		opt.callBack=alert;
		opt.queryH={test:"a中国--post--在aa",aaab:"你好吗？"};
		_MyMVC_ajax.get(url,opt);
	}
	
	function test2()
	{
		var opt={};
		opt.callBack=_MyMVC_debug_server;
		opt.method="POST";
		opt.insertId="result";
		opt.queryH={test:"a中国--post--在aa",aaab:"你好吗？"};
		_MyMVC_ajax.appForm("form1","yxh_test.ajax",opt);
	
	}
	function test3()
	{
		var opt={};
		opt.method="POST";	
		opt.insertId="result";
		opt.queryH={test:"a中国--post--在aa",aaab:"你好吗？"};
		_MyMVC_ajax.appForm("form1","yxh_test.ajax",opt);
	}
	
	function test4()
	{
		var opt={};
		opt.method="POST";
		opt.insertId="result";
		opt.handlerAgent="IFM";
		opt.callBack=_MyMVC_debug_server;
		opt.queryH={test:"a中国--post--在aa",aaab:"你好吗？"};
		_MyMVC_ajax.appForm("form1","yxh_test.ajax",opt);
	}
	
*/
//-----------------------------------------------------------------------
//-----------------------------------------------------------------------
var _MyMVC_ajax=
{
	ifmAgentId:0,
	ifmAgentName:"MyMVC_ajax_iframe_",//使用IFRAME模式时可用
	createXH:function ()
	{
		var x = false;
		try { x = new ActiveXObject("Msxml1.XMLHTTP"); }
		catch (e)
		{
			try { x = new ActiveXObject("Microsoft.XMLHTTP"); }
			catch (e) { x = false; }
		}
		if (!x && typeof(XMLHttpRequest) != 'undefined')
		{x = new XMLHttpRequest();}	
		return  x;	
	},	
	initopt:function (opt)
	{
		if (typeof(opt)!="object") {opt={};}
		if (typeof(opt.handlerAgent)=="undefined"){opt.handlerAgent="XMLHTTP";}
		if (typeof(opt.queryH)!="object")		{opt.queryH={};} 
		if (typeof(opt.async)=="undefined")		{opt.async=true;}					
		if (typeof(opt.insertId)=="undefined")	{opt.insertId=null;}			
		if (typeof(opt.method)=="undefined")	{opt.method="GET";}			
		if (typeof(opt.loading)!="object") 
			{opt.loading={start:function(){},end:function (){}};}						
		if (typeof(opt.callBack)!="function" && typeof(opt.callBack)!="object")
			{opt.callBack=function (v){};}				
		opt.queryH.mymvc_ajax_ext_data_temp_str=(new Date);//防止缓存
		return opt;
	},
	ifmRequest:function (url,opt,formId)
	{
		var _iframe=document.getElementById(this.ifmAgentId);
		if (null!=_iframe) _iframe.parentNode.removeChild(_iframe);
		this.ifmAgentId++;
		_iframe=document.getElementById(this.ifmAgentId);	
		var _ifName	= this.ifmAgentName+this.ifmAgentId;
		if (document.all)
		{_iframe = document.createElement("<iframe name='"+_ifName+"'></iframe>");}
		else 
		{
			_iframe = document.createElement("iframe");
			_iframe.name = _ifName;
		}
		_iframe.id	= _ifName;
		_iframe.style.display = 'none';
		document.body.appendChild(_iframe);	
		//----------------------------------		
		if (url!='') 
		{
			url+=(url.indexOf("?")==-1)?"?":"&";
			url+=this.hashToQuery(opt.queryH);
			if (opt.method=="POST")
			{
				if (formId==''){alert("使用IFM模式的POST方法请求数据必须通过表单");return false;}
				//表单设置并且提交
				form_obj=document.getElementById(formId);
				if (form_obj==null){alert("无法找到你要提交的表单...");return false;}				
				form_obj.enctype=(opt.method=="POST")?"multipart/form-data":"application/x-www-form-urlencoded";
				form_obj.action=url;//
				form_obj.method=opt.method;
				form_obj.target=_ifName;
				//alert("reach............"+_iframe.name);
				form_obj.submit();	
				opt.loading.start();
			}
			else
			{
				url+=(formId!='')?"&"+this.makeFormRequestStr(formId):"";
				_iframe.src = url;
				opt.loading.start();
			}
		}
		else {alert("请法URL不能为空...");return false;}
		//----------------------------------
		_MyMVC_addEvent(_iframe,"load",
						function ()
						{
							var ifDoc	=_iframe.contentWindow.document;
							var ret_v	=ifDoc.body.innerHTML;//alert("'"+ret_v+"' 'OK'");
							ifDoc.close();
							opt.loading.end();
							opt.callBack(ret_v);
							if (opt.insertId!=null)
							{	
								var o=document.getElementById(opt.insertId);
								if (o!=null) {o.innerHTML=ret_v;}
								else {alert("你的显示容器ID不存在");}
							}
						});
		//----------------------------------
	},
	xmlHttpRequest:function (url,opt,formId)
	{
		var XH=this.createXH();
		if (!XH){alert("无法创建XMLHTTP对象.");return false;}
		var	requestStrData="";
		if (opt.method=="POST")
		{
			requestStrData+=this.hashToQuery(opt.queryH);
			requestStrData+=(formId!='')?"&"+this.makeFormRequestStr(formId):"";			
		}
		else
		{
			url+=(url.indexOf("?")==-1)?"?":"&";
			url+=this.hashToQuery(opt.queryH);
			url+=(formId!='')?"&"+this.makeFormRequestStr(formId):"";
		}		
		//_MyMVC_out_test(url)
		XH.open(opt.method,url,opt.async);
		XH.setRequestHeader("CONTENT-TYPE","application/x-www-form-urlencoded");
		XH.onreadystatechange = function ()
		{
			if (XH.readyState == 1) {/*连接*/opt.loading.start();}
			if (XH.readyState == 2) {/*加载*/}
			if (XH.readyState == 4)
			{/*完成*/
				if (XH.status == 200)
				{
					opt.callBack(XH.responseText);
					if (opt.insertId!=null)
					{	
						var o=document.getElementById(opt.insertId);
						if (o!=null) {o.innerHTML=XH.responseText;}
						else {alert("你的显示容器ID不存在");}
					}
				}
				else
				{alert('HTTP通讯错误，错误代码为：' + XH.status);}
				opt.loading.end();
				XH=null;
			}		
		}
		XH.send(requestStrData);		
	},
	requestData:function (url,opt,formId)
	{
		opt=this.initopt(opt);//初始化处理请求选项
		if (opt.handlerAgent=="IFM"){this.ifmRequest(url,opt,formId);}
		else {this.xmlHttpRequest(url,opt,formId);}		
	},
	mvcModule:function (module,opt,moduleType,formId)
	{
		var act=(moduleType=="mvc")?_mvcACT:_appACT;
		var url=_webEntry+"?"+act+"="+module+"";
		this.requestData(url,opt,formId);	
	},	
	get			:function(url,opt){this.requestData(url,opt,'');},	
	formPost	:function (formId,url,opt){this.requestData(url,opt,formId);},	
	//appGet		:function (module,opt){this.mvcModule(module,opt,"app","");},
	//appForm		:function (formId,module,opt){this.mvcModule(module,opt,"app",formId);},
	//mvcGet		:function (module,opt){this.mvcModule(module,opt,"mvc",'');},	
	//mvcForm		:function (formId,module,opt){this.mvcModule(module,opt,"mvc",formId);},	
	hashToQuery	:function (hashObj)
	{
		var str=""
		if (typeof(hashObj)!="object") return hashObj;
		for (key in hashObj)
		{
		   if (str=="") str+=key+"="+encodeURIComponent(hashObj[key]);
		   else str+="&"+key+"="+encodeURIComponent(hashObj[key]);
		}
		return str;
	},
	makeFormRequestStr:function (formId)
	{
		var form_obj=document.getElementById(formId);
		if (form_obj==null) {alert("无法找到你要提交的表单.");return "";}
		var e_num=form_obj.elements.length;
		var rq_str="";
		for (i=0;i<e_num;i++)
		{
			var is_use=0;
			e_obj=form_obj.elements[i];
			var v_name=e_obj.name;
			var v_value=e_obj.value;
			if (e_obj.type=="radio" || e_obj.type=="checkbox")  
			{
				if (e_obj.checked==true)
				{
				  //alert("reach  radio checkbox");
				  if (rq_str=="") rq_str+=v_name+"="+encodeURIComponent(v_value);
				  else  rq_str+="&"+v_name+"="+encodeURIComponent(v_value);				  
				}
			
			}
			else if (e_obj.type=="select-multiple") 
			{
				v_name=v_name+"[]";
				v_arr=[];
				for(i=0;i<e_obj.options.length;i++)
				{
					if(e_obj.options[i].selected==true)
					{
						v_arr[v_arr.length]=e_obj.options[i].value;
						//alert(obj.options[i].value);
					}
				}				
				//alert("1 is "+e_obj.options[2].checked);
				for (j=0;j<v_arr.length;j++)
				{
					if (rq_str=="") rq_str+=v_name+"="+encodeURIComponent(v_arr[j]);
					else  rq_str+="&"+v_name+"="+encodeURIComponent(v_arr[j]);					  
				}
			}
			else
			{
				if (rq_str=="") rq_str+=v_name+"="+encodeURIComponent(v_value);
				else  rq_str+="&"+v_name+"="+encodeURIComponent(v_value);			  
			}
		}//end for...
		return rq_str;
	}
}
//-----------------------------------------------------------------------
//-----------------------------------------------------------------------
//动态引入包含文件
var _MyMVC_inc=
{
	css:function(path,reload)
	{
	  var scripts = document.getElementsByTagName("link"); 
	  if (!reload) 
	  for (var i=0;i<scripts.length;i++) 
			if (scripts[i].src && scripts[i].src.toLowerCase() == path.toLowerCase() ) return null; 
	  var sobj = document.createElement('link'); 
	  sobj.type = "text/css"; 
	  sobj.rel = "stylesheet"; 
	  sobj.href = path; 
	  var headobj = document.getElementsByTagName('head')[0]; 
	  headobj.appendChild(sobj); 		
	},
	js:function(path,reload)
	{		
	  var scripts = document.getElementsByTagName("script"); 
	  if (!reload) 
	  for (var i=0;i<scripts.length;i++) 
			if (scripts[i].src && scripts[i].src.toLowerCase() == path.toLowerCase() ) return null; 
	  
	  var sobj = document.createElement('script'); 
	  sobj.type = "text/javascript"; 
	  sobj.src = path; 
	  var headobj = document.getElementsByTagName('head')[0]; 
	  headobj.appendChild(sobj);
	}
}
//-----------------------------------------------------------------------
//cookies  操作
var _MyMVC_cookies=
{
	//-----------------------------------------------------------
	/*
	设置 Cookies
	使用实例
	.set("postfontsize", value, 30*86400*1000,"/bbs/");
	name   ---变量名
	value  ---值
	第三个可选参数：exp 有效时间 以秒为单位
	第四个可选参数：path 访问目录
	*/	
	set: function (name, value)
	{ 
		var exp = new Date();
		var argv = arguments;
		var argc = arguments.length;
		var expires = (argc > 2) ? (exp.setTime(exp.getTime() + parseInt(argv[2]))) : null;
		var path = (argc > 3) ? argv[3] : null;
		var domain = (argc > 4) ? argv[4] : null;
		var secure = (argc > 5) ? argv[5] : false; 
		
		document.cookie = name + "=" + escape (value) + ((expires == null) ? "" : ("; expires=" + expires.toGMTString())) + ((path == null) ? "" : ("; path=" + path)) + ((domain == null) ? "" : ("; domain=" + domain)) + ((secure == true) ? "; secure" : "");
	} ,
	//-----------------------------------------------------------
	get: function (name) 
	{
	  var arg = name + "=";
	  var alen = arg.length;
	  var clen = document.cookie.length;
	  var i = 0;
	  while (i < clen) {
		var j = i + alen;
		if (document.cookie.substring(i, j) == arg)
		{
			var offset=j;
			var endstr=document.cookie.indexOf (";",offset);
			if (endstr==-1) endstr=document.cookie.length;
			return unescape(document.cookie.substring(offset, endstr));
		}
		i = document.cookie.indexOf(" ", i) + 1;
		if (i == 0) break; 
	  }
	  return '';
	},
	//-----------------------------------------------------------
	del: function (name) 
	{
		var exp=new Date(); 
		exp.setTime (exp.getTime()-1); 
		var cval=this.get (name); 
		document.cookie=name+"="+cval+";expires="+exp.toGMTString();
	}
}
//-----------------------------------------------------------------------
//检查
var _MyMVC_check=
{
	isMobile:function (number)
	{
		var rStr = new RegExp("[^0-9]", "g");
		if(number.match(rStr)) return false;
		if (number.length!=11) return false
		return true;
	},
	isDate:function (year, month, day)  
	{
		var rc = true;
		year = parseInt(year,10);
		month = parseInt(month,10);
		day = parseInt(day,10);
		
		if((year < 1900) || (month < 1) || (month > 12) || (day < 1) || (day > 31))
		return false;
		switch (month) {
		case 1 :
		case 3 :
		case 5 :
		case 7 :
		case 8 :
		case 10:
		case 12:
		  if (day >31)
			rc = false;
		  break;
		
		case 4 :
		case 6 :
		case 9 :

		case 11:
		  if (day >30)
			rc = false;
		  break;
		case 2 :
		  if ( (year%4 == 0) && (year%100 != 0) || (year%400 == 0) ) {
			if( day > 29)
			  rc = false;
		  }
		  else {
			if( day >28)
			  rc = false;
		  }
		  break;
		default :
		  rc = false;
		}
		return rc;
	},
	isEmail	: function (email) 
	{
		var rStr = new RegExp("[^a-z,0-9,_,--,@,\.]", "ig");
		if((!email.match(rStr))&&email.length>5&&email.indexOf('@')>0&&email.indexOf('.')>0)
		return true;
		else
		return false;
	},
	isNumber:function (number) 
	{
		var number=new String(number);
		var rStr = new RegExp("^-?[0-9]+$", "g");
		if(number.match(rStr))
		return true;
		else
		return false;
		
	},
	isUserName:function (name) 
	{
		var partern=/^[A-Za-z0-9_]+$/; 
		return this.regExp (name,partern);
	},
	regExp:function (str,q)
	{// q=/[\u4e00-\u9fa5]/;
		if (q.test(str)) return true;	
		else return false;
	},
	isNull:function (str)
	{//不能为空,不能包括特殊符号
		if (str=="") return true;
		var q1=/^[\s]+$/;
		return this.regExp(str,q1);
	},
	isSpecialChar:function (str)
	{
		var q=/[\\\+\=\|\~\!\@\#\$\%\^\&\*\(\)\{\}\[\]\-\?\>\<\,\.\/]/;
		return this.regExp(str,q);
	},
	isTel:function (str)
	{
		var q=/^[0-9_]+$/; 
		return this.regExp(str,q);
	}
	
}
//-----------------------------------------------------------------------
//表单操作类
function  _MyMVC_form(formId)
{
}
//-----------------------------------------------------------------------
function _MyMVC_addEvent(obj, evType, fn)
{//对象，事件（没有on），函数
	if (obj.addEventListener)
	{
		obj.addEventListener(evType, fn, true);
		return true;
	} 
	else if (obj.attachEvent)
	{return  obj.attachEvent("on"+evType, fn);}
	else {return false;}
}
//-----------------------------------------------------------------------
//获取URL地址上的 GET 参数
function _MyMVC_GET(key)
{
   var sSearch;
   var aPairs;
   var i;
   sSearch = (document.location.search.length > 1) ? document.location.search.substring(1) : "";
   if (sSearch != "")
   {
	  aPairs = sSearch.split("&");
	  for (i =0;i <aPairs.length;i++)
	  {
		 var tem_arr=aPairs[i].split("=");
		 if (tem_arr[0]==key){return tem_arr[1];}				 
	  }
   }
   return "";
}
//-----------------------------------------------------------------------
//转化JSON字符串
function _MyMVC_jsonObj(jsonStr)
{
	try
	{
		//alert(jsonStr);
		jsonStr=new String(jsonStr);
		jsonStr=jsonStr.replace(/\s/ig,'  '); 
		eval("var _MyMVC_temp_var="+jsonStr+";");		
	}
	catch(e)
	{
		var lineS	="\n===========================================================\n";
		var debugS	="JSON数据："+lineS+jsonStr+lineS+"\n\n\n";
		var msgS	="系统出现错误，可能是系统出现BUG或者非法操作.";
		
		if (_MyMVC_INI.isDebugMod>0) {msgS=debugS+msgS;}
		alert(msgS);
		return false;	
	}
	return 	_MyMVC_temp_var;
}
//-----------------------------------------------------------------------
function _MyMVC_callBackCheck(jsonStr)
{
	if (_MyMVC_INI.isDebugMod>1) { _MyMVC_debug_server(jsonStr); }//调试测试
	var o=_MyMVC_jsonObj(jsonStr);
	if (typeof(o)=="object")
	{
		if (o.status=="OK") return o;
		else
		{
			alert(o.status);
			return false;			
		}			
	}
}
//-----------------------------------------------------------------------
function _MyMVC_debug_server(str)
{//调试数据信息显示
	//alert(str);
	var o=document.getElementById(_MyMVC_INI.debugPanel);//  out_test
	if (o==null)
	{
		o=document.createElement("DIV");
		o.id = _MyMVC_INI.debugPanel;
		o.title="提示：双击关闭调试信息";
		o.style.backgroundColor="#e6e6e6";
		function closeDebugPanel()
		{
			o.style.display="none";
		}		
		document.body.appendChild(o);
		_MyMVC_addEvent(o,"dblclick",closeDebugPanel)	
	}
	if (o!=null){o.style.display="";o.innerHTML=str;}	
}
//-----------------------------------------------------------------------
/*
语言包的使用：
js  必含  _MyMVC_LANG["pageName_XXXX"] 语言数组
php 必含 $_MyMVC_LANG["pageName_XXXX"] 语言数组
都有共同的调用接口： _LANG_O
第一个参数是语言包索引
第二个以后将替换语言数据中的 #1# #2# ....
*/
function _LANG_O (index)
{
	if (_MyMVC_LANG=="undefined") 
	{alert("无法找到语言信息，可能是语言包导入失败.");return false;}
	var arg_n=arguments.length;
	if (arg_n==1) return _MyMVC_LANG[index];
	else
	{
		var tmp=_MyMVC_LANG[index];
		for (i=1;i<arg_n;i++)
		{tmp=str_replace(tmp,"#"+i+"#",arguments[i]);}				
	}
	return tmp;	
	
}//end var te=_LANG_O("web_nav_01");alert(te);
//-----------------------------------------------------------------------
function openDialog(url,defValue,w,h)
{
	
	h=parseInt(h);
	w=parseInt(w);
	var openStr="dialogWidth:"+2+"px;dialogHeight:"+h+"px;status:no;help:no;";
	return showModalDialog(url,defValue,openStr);	
}
//-----------------------------------------------------------------------
//字符串替换方法
function str_replace(str,a,b) 
{ 
	if (b=="" || b.indexOf(a)!=-1) return str;
	var i; 
	var s2 = str; 	
	while(s2.indexOf(a)>0) 
	{ 
		i = s2.indexOf(a); 
		s2 = s2.substring(0, i)+b+s2.substring(i+ b.length,s2.length); 
	} 
	return s2; 
} //end str_replace
//-----------------------------------------------------------------------
function autoSizeImage(ImgD,w,h)
{
  //alert('reach..');
  try
  {
	 var image=new Image(); 
	 var iwidth = w;  //定义允许图片宽度 
	 var iheight = h;  //定义允许图片高度 
	 image.src=ImgD.src; 
	 if(image.width>0 && image.height>0)
	 { 
		 flag=true; 
		 if(image.width/image.height>= iwidth/iheight)
		 { 
			  if(image.width>iwidth)
			  {   
				  ImgD.width=iwidth; 
				  ImgD.height=(image.height*iwidth)/image.width; 
			  }
			  else
			  { 
				  ImgD.width=image.width;   
				  ImgD.height=image.height; 
			  } 

		} 
		else
		{ 
			 if(image.height>iheight)
			 {   
				  ImgD.height=iheight; 
				  ImgD.width=(image.width*iheight)/image.height;   
			  }
			  else
			  { 
				  ImgD.width=image.width;   
				  ImgD.height=image.height; 
			  } 
			
		  } 
	 } 
  }
  catch (e)
  {
	alert(e);
  }

}  //end AutoSizeImage
//-----------------------------------------------------------------------
if (_MyMVC_INI.noMenu)   _MyMVC_addEvent(document,"contextmenu",new Function("event.returnValue=false;"));
if (_MyMVC_INI.noSelect) _MyMVC_addEvent(document,"selectstart",new Function("event.returnValue=false;"));
//-----------------------------------------------------------------------
if (_MyMVC_INI.isDebugMod>0)
{
	_MyMVC_addEvent(window,"error",	
		function (sMsg,sUrl,sLine)
		{
			oErrorLog="<b>系统JS发生错误：.</b><hr><p>";
			oErrorLog+="Error: " + sMsg + "<br>";
			oErrorLog+="Line: " + sLine + "<br>";
			oErrorLog+="URL: " + sUrl + "<br>";
			_MyMVC_debug_server(oErrorLog);
			alert("系统JS发生错误,请查看页面底部的错误信息。");
			event.returnValue=false;
			return false;
		});

}
//-----------------------------------------------------------------------
