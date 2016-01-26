//----------------------------------------------------------------------------
/*
*****************************
yxh0612@163.com js_lib * 通用的联动下接菜单JS类
Lastdate：2006-02-21 22:58
QQ：3906261(夜之子,飞飞)
Copyright：Doublefly 叶雄辉
*****************************

使用方法：
//------------------------------ 　定义数据源 -----------
//数据格式： ID，父级ID，名称[ ，扩展一，扩展二 ... 可以有无限个扩展数据]
var array2=new Array();//数据格式 ID，父级ID，名称[ ，扩展一，扩展二 ... 可以有无限个扩展数据]
array2[0]=new Array("测试测试","根目录","测试测试","扩展参数测试1","扩展参数测试22"); 
array2[1]=new Array("华北地区","根目录","华北地区","扩展参数测试2","扩展参数测试22");
array2[2]=new Array("上海","测试测试","上海","扩展参数测试3");
array2[3]=new Array("广东","测试测试","广东","扩展参数测试4");
array2[4]=new Array("徐家汇","上海","徐家汇","扩展参数测试5");
array2[5]=new Array("普托","上海","普托","扩展参数测试6");	
array2[6]=new Array("广州","广东","广州","扩展参数测试7");
array2[7]=new Array("湛江","广东","湛江","扩展参数测试8");
array2[8]=new Array("不知道","湛江","不知道","扩展参数测试9");
array2[9]=new Array("5555","湛江","555","扩展参数测试10");
array2[10]=new Array("++++","不知道","++++","扩展参数测试11");
array2[11]=new Array("111","徐家汇","111","扩展参数测试12");
array2[12]=new Array("222","111","222","扩展参数测试13");
array2[13]=new Array("333","222","333","扩展参数测试14");

//------------------------------ 以上是数据源 -----------
var test_obj;//测试对象
test_obj=new CWDN_LinkageClass(data=array2,panle_id="根目录");
test_obj.setHideSelect(1);//隐藏不启用的SELECT 最好在加载SELECT之设置
test_obj.setSelectDefault(def_name="我的选择",def_value="");//初始的的值
test_obj.setSelectObjs("test_select","x1","x2","x3");//接顺序专入，可以有任意个
test_obj.setOnfocusInterface(interfaceTest);//onfocus 接口
test_obj.setOnchangeInterface(interfaceTest);//onchange　接口

var testextra=test_obj.getExtraValue(v=0,v_index=2,type="index");//扩展数据的获取
alert(type + "为 "+v+" 的第 "+v_index+" 个扩展数据为:"+testextra);
var testextra=test_obj.getExtraValue(v="test_select",v_index=1,type="id");
alert(type + "为 "+v+" 的第 "+v_index+" 个扩展数据为:"+testextra);

//接口测试函数---------
function interfaceTest(obj)
{
  //alert("type is "+obj.type+"  value is "+obj.value);
  myid=obj.options[obj.selectedIndex].myid;
  alert("myid is "+myid);
  //alert("扩展参数：");
}  
*/
//----------------------------------------------------------------------
//类的定义开始
//----------------------------------------------------------------------
//类的定义开始 可以打包为 .js 文件
function CWDN_LinkageClass(data,root_id)
{
	//------------------------------
	this.data=data;//总数据
	this.selectObjs=Array();//下接列表对象数组	
	this.root_id=root_id;
	this.def_name="请选择";//下拉菜单的默认值
	this.def_value="";//下拉菜单的默认值
	this.ishide=0;//设置是否隐藏未启用的Select
	//------------------------------
	//将所有Select ID 载入
	//可以设置任意个SELECT 以ID　为参数
	this.setSelectObjs=function ()
	{
	   this.selectObjs=arguments;
	   var se_obj;
	   for (i=0;i<arguments.length;i++)
	   {
	     se_obj=document.getElementById(arguments[i]);
		 if (se_obj!=null)
		 {//初始化下接菜单
		   se_obj.objIndex=i;//当前下拉菜单的索引值
		   var me=this;
           se_obj.onchange=function() {me.onchangeHander(this.objIndex,this.value,this);}
		   se_obj.onfocus=function() {me.onfocusHander(this.objIndex,this);}
		 }
		 else
		 {
		    var msg=" 系统未能初始化对象，\n\n 你所设置的第 "+(i+1)+"参数错误。";
			msg+="参数错误。\n\n ID为：[\""+arguments[i]+"\"] 的对象无法初始化。";
			alert(msg);
		 }
	   }//end for 
	   this.chgFromDeepSelect(0,this.root_id);
	   //alert(this.selectObjs[100]);
	}//end setSelectObjs
	//------------------------------
	//------------------------------
	//下接菜单获取焦点时的接口
	this.onfocusHander=function (index,vobj)
	{
		for (i=0;i<index;i++)
		{
		   var obj=document.getElementById(this.selectObjs[i]);
		   if (obj.selectedIndex==0)
		   {
		     alert("你还没有选择上一级菜单，请先选择.");
			 obj.focus();
			 break;
		   }
		}
		this.onfocusInterface(vobj);	   
	}//end onfocusHander
	//------------------------------
	//下接菜单的Onchange接口
	this.onchangeHander=function (index,value,obj)
	{
	   this.chgFromDeepSelect(index+1,value);
	   this.onchangeInterface(obj);
	}//end onchangeHander
	//------------------------------
	//从某个深度开始初始化下接菜单
	this.chgFromDeepSelect=function (index,pare_id)
	{
		 //到了最后一个选择项
		 if (index>=this.selectObjs.length) return;
		 for (i=index;i<this.selectObjs.length;i++)
		  {//初始化由此以下的所有节点
		    this.resetSelect(this.selectObjs[i]);
			//设置隐藏与显示
			if (i==index) this.showSelect(i);
			else this.hideSelect(i);
		  }
		 this.setSelectDdata(index,pare_id);
		  
	}// end 	chgFromDeepSelect
	//------------------------------
	//根据值选定一个Slecect的Option
	this.setSelectOption =function (index,v)
	{
	     var obj=document.getElementById(this.selectObjs[index]);
		 var vdata=obj.options;
		 for (i=0;i<vdata.length;i++)
		 {
		    if (vdata[i].value==v)
			{
			   obj.options[i].selected=true;break;
			}		  
		 }
	}	
	//------------------------------
	//设置一个下接菜单的内容
	this.setSelectDdata=function (index,pare_id)
	{
	     var obj=document.getElementById(this.selectObjs[index]);
		 this.resetSelect(this.selectObjs[index]);//重设
		 this.showSelect(index);		 
		 var vdata=this.getChilds(pare_id);
		 for (i=0;i<vdata.length;i++)
		 {
		   var opt=new Option(vdata[i][2],vdata[i][0]);
		   opt.myid=vdata[i][vdata[i].length-1];
		   obj.options[obj.length]=opt;
		 }	
	}// end 	setSelectDdata
	//------------------------------
	//重置一个Select 内容
	this.resetSelect =function (s_id)
	{
	   var obj=document.getElementById(s_id);
	   var length=obj.options.length;
	   while(length!=0)
	   { 
		 for(var i=0;i<length;i++) {obj.options.remove(i);}
		 length=length/2;
	   }
	  obj.options[0]=new Option(this.def_name,this.def_value);
	}
	//------------------------------
	//设置第一项的onption标签值
	this.setSelectDefault =function (def_name,def_value)
	{
	   this.def_name=def_name;
	   this.def_value=def_value;
	}//end setSelectDefault
	//------------------------------
	//由某一节点的值查找它的父结点
	//返回一个数组，与数据源的定义结构一样
	//数据格式： ID，父级ID，名称[ ，扩展一，扩展二 ... 可以有无限个扩展数据]
	this.getParentNode=function (v)
	{
	    var length=this.data.length;
		var pare=Array();
		for (i=0;i<length;i++)
		{
		   if (this.data[i][0]==v)
		   {
		      pare=this.data[i];
			  break;			  		
		   }
		}
		return pare;
	}
	//------------------------------
	//获取某一节点的第一代子节点
	//数据格式： ID，父级ID，名称[ ，扩展一，扩展二 ... 可以有无限个扩展数据]
	this.getChilds=function (pare_id)
	{
	    var length=this.data.length;
		var child=Array();
		for (i=0;i<length;i++)
		{
		   if (this.data[i][1]==pare_id)
		   {
		      child[child.length]=this.data[i];
			  child[child.length-1][child[child.length-1].length]=i;		
		   }
		}
		return child;
	}//end getchidls
	//------------------------------
	//提供给外界的 onfocus 接口
	this.onfocusInterface = function (obj){}	
	//------------------------------
	//提供给外界的 onfocus 设置接口
	this.setOnfocusInterface = function (func)
	{
	   if (typeof(func)=="function") this.onfocusInterface=func;
	   else
	   {
	      alert("定义onfocusInterface 接口时出错，请检查你的参数。");
	   }	   
	}//end setOnfocusInterface
	//------------------------------
	//提供给外界的 onchange 接口
	this.onchangeInterface = function (obj){}	
	//------------------------------
	//提供给外界的 onfocus 设置接口
	this.setOnchangeInterface = function (func)
	{
	   if (typeof(func)=="function") this.onchangeInterface=func;
	   else
	   {
	      alert("定义onchangeInterface 接口时出错，请检查你的参数。");
	   }	   
	}//END setOnchangeInterface
	//------------------------------
	//是否隐藏未能启用的Select　
	//如果设置隐藏，则Select　会动态的出现
	//默认不隐藏, 1 为隐藏　0为不隐藏
	this.setHideSelect = function (ishide)
	{
	   this.ishide=ishide;
	}//end isHideSelect
	//------------------------------
	//隐藏
	this.hideSelect = function (index)
	{
	   if (this.ishide==1)
	   {
	     var obj=document.getElementById(this.selectObjs[index]);
		 obj.style.display="none";
	   }
	}
	//显示
	this.showSelect = function (index)
	{
	   if (this.ishide==1)
	   {
	     var obj=document.getElementById(this.selectObjs[index]);
		 if (index>0)
		 {
		    var preobj=document.getElementById(this.selectObjs[index-1]);
			if (preobj.selectedIndex!=0) obj.style.display="";
			else  obj.style.display="none";
		 }
		 
	   }
	}
	//------------------------------
	//在数据源的结构中从第四个数据开始被称为可扩展数据
	//数据格式： ID，父级ID，名称[ ，扩展一，扩展二 ... 可以有无限个扩展数据]
	//如果 type = id 时 v　要传入 id 
	//如果 type 为 index　时 v 专入索引值　是从0开始的
	//v  可能是联动菜单的萦引或者ID
	//v_index　是从1开始的，obj.getExtraValue("select_id",1);
	//是表示取第一个扩展数据
	this.getExtraValue = function (v,v_index,type)
	{
	   if (this.selectObjs=="") {alert("分类系统还未初始化.......");return;}
	   var obj;
	   var ret=null;
	   if (type=="id") obj=document.getElementById(v);
	   else if (type=="index") obj=document.getElementById(this.selectObjs[v]);
	   else
	   {alert("参数错误，TYPE　只能是　id 或者 index ");return null;}
	   if (obj.selectedIndex==0) return null;
	   try
	   {
	     myid=obj.options[obj.selectedIndex].myid;
		 if (myid==null) return null;
		 ret=this.data[myid][v_index+2];
	   }
	   catch(e)
	   {alert("无法找到扩展数据的ID容器，错误信息为："+e.description);return null;}
	   return ret;	   	
	}//end getExtraValue
	//------------------------------
	//初始化联动菜单的选定值
	
	//v 为可能的参数，可能是一个字符中，或者数组
	//type 可能为 from_start from_end
	//为 from_start 时，v 是一个从零开始的数组，依次是每个要选定的Select 的值
	//为 from_end 时，v 是一个联动选择菜单中的最后一个选定值
	
	//使用此方法时 数据源中的值必须为唯一的
	
	this.setSelectValues = function (v,type)
	{
	   if (this.selectObjs=="") {alert("分类系统还未初始化.......");return;}
	   if (type=="from_start" && typeof(v)=="object")    
	   {
	      if (v.length>this.selectObjs.length)
		  {
		     alert("参数错误，你给定的初始化值的级别数大于你初始化联动菜单所指定的级别");
			 return
		  }
		  else
		  {
			 for (set_i=0;set_i<v.length;set_i++)
			 {
			   this.setSelectOption(set_i,v[set_i]);
			   //this.showSelect(set_i);
			   this.chgFromDeepSelect(set_i+1,v[set_i]);	
			   //alert(set_i);			   
			   //alert(v[set_i]);		   
			 }
		  }
	   }
	   else if (type=="from_end" && typeof(v)!="object")
	   {
	      //从最后一个选择项开始选
		  var set_index=this.selectObjs.length-1;//一共有多少个下接菜单-1
		  var pare=this.getParentNode(v);		  
		  if (pare=="")
		  {
		     alert("系统找不到你要设置的值： "+v);return;
		  }
		  var pareid=pare[1];//父ID
		  var myid=pare[0];//自ID
		  
		  var set_arr=Array();		  
		  while (set_index>=0)
		  {
			 set_arr[set_index]=myid;
			 if (this.root_id == pareid) break;
			 pare="";//清空
			 var pare=this.getParentNode(pareid);
			 if (pare==""){alert("你设置的参数错误，或者数据链已被破坏");return;break}
			 else
			 {
			   pareid=pare[1];//父ID
		       myid=pare[0];//自ID
			   
			   set_index--;				   	   
			 }
		   }
		   this.setSelectValues(set_arr,type="from_start");
		   /**/
		  
	   }
	   else
	   {
	      alert("无法设定下接菜单组的初始值，请检查");return;
	   }
	
	}// end 	setSelectValues
	
	//------------------------------
}//end class CWDN_LinkageClass 类定义完成 
//----------------------------------------------------------------------------