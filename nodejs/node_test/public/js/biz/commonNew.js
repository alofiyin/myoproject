//----------------------------------------------------------
var ua = navigator.userAgent.toLowerCase(), bzi;
var binfo =
{
    ie : /*@cc_on!@*/false,
	i7 : /*@cc_on!@*/false && (parseInt(ua.match(/msie (\d+)/)[1],10) >= 7)
};
//----------------------------------------------------------
var __mymvcTools =
{
	//自增长属性
	myIndex:5000,
	//获取一个自增长的整数，用于层级，等数值控制
	getZindex : function()	{return ++this.myIndex;},
	//设置一个元素的透明度
	stopac : function( e, opac )
	{//设置透明度
	    if( binfo.ie )
		{
		    opac = Math.round( opac * 100 );
			e.style.filter = ( opac > 100 ? '' : 'Alpha(opacity=' + opac + ')' );
		}
		else
		    e.style.opacity = opac;
	},	
	//设置元素的样式
	ststyle : function( e, dict )
	{
	    var style = e.style;
		for( var n in dict ) style[n] = dict[n];
	},
	//生成一个空操作串
	getvoid : function()
	{
	    if( binfo.ie )
		    return ( binfo.i7 ? '' : 'javascript:\'\'' );
		return 'javascript:void(0)';
	},	
	//增加一个绑定事件
	addevt : function( o, e, l )
	{
	    if( binfo.ie )
		    o.attachEvent( 'on' + e, l );
		else
		    o.addEventListener( e, l, false );
	},	
	//删除一个绑定的事件
	remevt : function( o, e, l )
	{
	    if( binfo.ie )
		    o.detachEvent( 'on' + e, l );
		else
		    o.removeEventListener( e, l, false );
	},	
	//检查是否DTD
	isdtd : function(doc)
	{
	    return ( 'CSS1Compat' == ( doc.compatMode || 'CSS1Compat' ) );
	},	
	//获取客户端可视页面大小
	getclsize : function(w)
	{
		if( binfo.ie )
		{
		    var oSize, doc = w.document.documentElement;
			oSize = ( doc && doc.clientWidth ) ? doc : w.document.body;
			
			if(oSize)
			    return { w : oSize.clientWidth, h : oSize.clientHeight };
			else
			    return { w : 0, h : 0 };
		}
		else
		    return { w : w.innerWidth, h : w.innerHeight };
	},
	//获取客户端页面大小
	getssize : function()
	{
		var tdoc=document;
		var rel = this.isdtd(tdoc) ? tdoc.documentElement : tdoc.body;
		return {w:Math.max( rel.scrollWidth, rel.clientWidth, tdoc.scrollWidth || 0 ),
				 h:Math.max( rel.scrollHeight, rel.clientHeight, tdoc.scrollHeight || 0 )
				};
	},
	//获取滚动条位置
	getspos : function(w)
	{
	    if( binfo.ie )
		{
		    var doc = w.document;
			var oPos = { X : doc.documentElement.scrollLeft, Y : doc.documentElement.scrollTop };
			if( oPos.X > 0 || oPos.Y > 0 ) return oPos;
			return { X : doc.body.scrollLeft, Y : doc.body.scrollTop };
		}
		else
		    return { X : w.pageXOffset, Y : w.pageYOffset };
	},
	setDisplayCenter : function (oSelector)
	{
		var s=this.getspos(window);
		var cl=this.getclsize(window);
		var w=$(oSelector).width();
		var h=$(oSelector).height();
		var l=Math.max((cl.w-w)/2+s.X,0);
		var t=Math.max((cl.h-h)/2+s.Y,0);
		$(oSelector).css({position:"absolute",left:l,top:t});
	},
	//生成一个CSSLINK
	getCssLink : function(c)
	{
	    if( c.length == 0 ) return;
		return '<' + 'link href="' + c + '" type="text/css" rel="stylesheet"/>';
	},
	//获取当前样式值
	getestyle : function( e, p )
	{
	    if( binfo.ie )
		    return e.currentStyle[p];
		else
		    return e.ownerDocument.defaultView.getComputedStyle(e, '').getPropertyValue(p);
	},
	//删除一个节点
	remnode : function(n){ if(n) return n.parentNode.removeChild(n);},
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
	//生成MYMVC的请求URL
	ajaxUrl:function (module,data,isJSONP)
	{
		var d = data	|| {};
		var hS="";
		if (isJSONP) {hS+="&jsoncallback=?"}
		if (d!={}){hS+="&"+this.hashToQuery(d);}
		return module+""+hS;	
	},
	//提交表单到指定模块，并上传文件
	upFile:function (formSelector,module,cbFunc,data)
	{
		var d = data || {};
		var _ifmName="_mymvc_upfile_ifm"+this.getZindex();
		$("<iframe name='"+_ifmName+"' id='"+_ifmName+"'></iframe>").appendTo("body");
		$("#"+_ifmName).css({display: 'none'});
		$("#"+_ifmName).load(function (){
							   var ifDoc	=$("#"+_ifmName).get(0).contentWindow.document;
							   var ret_v	=ifDoc.body.innerHTML;//alert("'"+ret_v+"' 'OK'");
							   ifDoc.close();
							   cbFunc(ret_v);
							   });
		//表单设置并且提交
		$(formSelector).attr("enctype","multipart/form-data");
		$(formSelector).attr("action",this.ajaxUrl(module,d)); 
		$(formSelector).attr("method","POST");
		$(formSelector).attr("target",_ifmName);
		$(formSelector).submit();
	},
	//获取地址上的参数，参数可选
	_GET:function (key,parseUrl)
	{
		var k		=key || false;
		var uStr	=parseUrl|| document.location;
		
		var isSet	=uStr.match(/\?([^#]+)/i);
		if (!isSet) {return k?{}:'';}
		var aPairs	=isSet[1].split("&");
		var r={};
		for (i =0;i <aPairs.length;i++)
		{
			var tmp=aPairs[i].split("=");
			r[tmp[0]]=tmp[1];
		}
		return k?r[k]:r;
	},	
	///url编码转换
	hashToQuery	:function (hashObj,isEncode)
	{
		var enC=isEncode || false;
		var str=""
		if (typeof(hashObj)!="object") return hashObj;
		for (key in hashObj)
		{
		   if (str=="") str+=key+"="+(isEncode?encodeURIComponent(hashObj[key]):hashObj[key]);
		   else str+="&"+key+"="+(isEncode?encodeURIComponent(hashObj[key]):hashObj[key]);
		}
		return str;
	},
	//全局的改变验证码的函数接口
	chgRandNum:function (oSelector)
	{
		//alert(oSelector);
		var u=$(oSelector).attr('src');
		var p=u.match(/^([^?]+)(?:\?([^#]*))?(\#.+)?$/i);
		var q=this._GET(false,u);
		q._mymvcRandNum=Math.random();
		$(oSelector).attr('src',p[1]+"?"+this.hashToQuery(q,false));
	},
	ckNoInterFace:function (sImg,sInput,sReset)
	{
		var self=this;
		$(sInput).focus(function (){self.chgRandNum(sImg);});
		$(sImg).click(function (){self.chgRandNum(sImg);});
		//alert($(sReset).length);
		$(sReset).attr('href','javascript:__mymvcTools.chgRandNum(\''+sImg+'\')');
	},
	///字符串长度
	strBitLen:function (s)
	{
		var st=new String(s);	
		var l = 0; 
		var a = s.split(""); 
		for (var i=0;i<a.length;i++){l+=(a[i].charCodeAt(0)<299)?1:2;}
		return l;
	}
};//__mymvcTools

//------------------------------------------------------------------
//显示一个标签容器，或者控件,基于 __mymvcTools JQUERY
/*
oSelector	//想显示的选择器
//opt 为可选项
opt.isM		//是否有庶罩层 默认值:false
opt.opac	//有庶罩层,s可设置其透明度 默认值:0.25
opt.pos		//设置目标显示后的位置 如： {left:10,top:20}
opt.isCenter//设置层显示后是否屏幕居中[一定要选true]
opt.showFunc//设置层显示方式，默认无特效，可由用户显示特效

__mymvcTools.show("#test");
*/
function __mymvcShow(oSelector,opt)
{
	var myopt	=opt		|| {};
	var isM		=myopt.isM	|| false;	//是否有庶罩层
	var opac	=myopt.opac	|| 0.25;	//透明度
	var setPos	=myopt.pos	|| false;	//显示后的位置如： {left:10,top:20}
	var isCenter=myopt.isCenter	|| false;
	var showFunc=myopt.showFunc	|| function (){$(oSelector).show();};
	
	var clsize	=__mymvcTools.getssize(window);
	var ssize	=__mymvcTools.getspos(window);
	var zindex	=[__mymvcTools.getZindex(),__mymvcTools.getZindex(),__mymvcTools.getZindex()];	
	
	var mId		="_mymvc_mark_div"+zindex[0];
	var dId		="_mymvc_dfm_div"+zindex[1];
	var myAttr	="_mymvc_show_attr";
	//-----------------------------------	
	if (isCenter) {__mymvcTools.setDisplayCenter(oSelector);}
	//-----------------------------------	
	if (setPos) {$(oSelector).css(setPos);}
	//-----------------------------------
	$(oSelector).css({zIndex:zindex[2]});
	$(oSelector).attr(myAttr,zindex.join(","));
	//-----------------------------------
	//用于解决SELECT控件问题的容器CSS
	var ifmDivCss={
		zIndex:zindex[1],position:"absolute",
		left:0,top:0,width:clsize.w,height:clsize.h,
		filter	: 'progid:DXImageTransform.Microsoft.Alpha(opacity=0)'
	};
	//设置遮罩层
	if (isM){
		$("<div id='"+mId+"'></div>").appendTo("body");//filter:"Alpha(opacity=25);",opacity:"0.25",	
		$("#"+mId).css({left:"0px",top:"0px",backgroundColor:"#000000",zIndex:zindex[0],position:"absolute"});
		$("#"+mId).width(clsize.w);
	  	$("#"+mId).height(clsize.h);
		__mymvcTools.stopac($("#"+mId).get(0),opac);
	}
	else{
		$(oSelector).css({display:'block'});
		ifmDivCss={
			zIndex:zindex[1],position:"absolute",
			left:$(oSelector).offset().left,
			top:$(oSelector).offset().top,
			width:$(oSelector).width()+10,
			height:$(oSelector).height()+10,
			filter	: 'progid:DXImageTransform.Microsoft.Alpha(opacity=0)'
		};
		$(oSelector).css({display:'none'});
	}
	//-----------------------------------		
	//添加隐藏的IFRAME
	if( binfo.ie && !binfo.i7 ){
		var ifmDiv='<div id="'+dId+'"></div>';
		$(ifmDiv).insertBefore(oSelector);
		$("#"+dId).css(ifmDivCss);
		var ifmHtml='<iframe style="width:100%;height:100%"></iframe>';
		$(ifmHtml).appendTo("#"+dId);
		$("#"+dId+' iframe').attr('src',__mymvcTools.getvoid());
	}
	//-----------------------------------
	showFunc();	
	//-----------------------------------
};
__mymvcTools.show=__mymvcShow;
//----------------------------------------------------------
//内置的层显示关闭 
/*
oSelector //要控制显示的目标容器
closeFunc //关闭接口

实例：
function Test2()
{
	var oSelector='#apDiv1';//要控制显示的目标容器
	//关闭接口 可选参数
	var closeFunc=function () {$("#apDiv1").slideUp();};
	__mymvcHide('#apDiv1',closeFunc);
}
*/
function __mymvcHide(oSelector,closeFunc)
{
	var closeFunc=closeFunc|| function (){$(oSelector).hide();};
	var myAttr	="_mymvc_show_attr";
	$(oSelector).each(function (){
		var zindex	=$(this).attr(myAttr);
		if (zindex)
		{
			zindex=zindex.split(",");
			var mId		="#_mymvc_mark_div"+zindex[0];
			var dId		="#_mymvc_dfm_div"+zindex[1];
			$(mId+","+dId).remove();		
		}
		closeFunc();/**/
	});
	
	
}
__mymvcTools.hide=__mymvcHide;
//----------------------------------------------------------
//cookies  操作
var __mymvcCookies=
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
__mymvcTools.CK=__mymvcCookies;

//-----------------------------------------------------------------------
/*
全局的，用于控制多选的接口使用说明：

初始化一个控制接口：

	参数说明：
	checkName
		被控制的多选输入控件的名称，即 name 属性，
		所有被控制的多选控件使用同一个名称
		
	selector
		控制全选的控件选择器，是一个 checkbox，点击它实现全选 
	
	
	inSelector 参数可选
		控制反选的控件选择器，点击它实现反选
		
	__mymvcTools.selCHK.(checkName,selector[,inSelector]);

获取选中的值
	参数说明：
	checkName
		被控制的多选输入控件的名称，即 name 属性，
		所有被控制的多选控件使用同一个名称	
	isToString 参数可选
		不提供这个参数将返回一个值的数组，
		如果提供，则返回一个用 isToString 相连的值的字符串
		
	__mymvcTools.selCHK.getValues(checkName[,isToString]);
*/
__mymvcTools.selCHK=
{
	//初始化一个全选控制类
	init:function (checkName,selector,inSelector)
	{
		$(selector).click(function (){
			var ck=$(this).attr("checked");
			var chk='input[type=checkbox][name="'+checkName+'"]';
			$(chk).each(function(){$(this).attr("checked",ck);});	
			
		});
		
		if (inSelector)
		{
			$(inSelector).click(function (){
				var chk='input[type=checkbox][name="'+checkName+'"]';
				$(chk).each(function(){
					$(this).attr("checked",!$(this).attr("checked"))
					
				});	
			});			
		}
	},
	getValues:function (checkName,isToString)
	{
		var t=[];
		var ist=isToString || false;
		var chk='input[type=checkbox][name="'+checkName+'"]';
		$(chk).each(function(){
			if ($(this).attr("checked")){t.push($(this).val());}				
		});		
		return ist?t.join(ist,t):t;		
	}
};
//-----------------------------------------------------------------------