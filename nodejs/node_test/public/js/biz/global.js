
$(document).ready(function(){
	var global_member_url = $("#global_member_url").val();
	///加载头部信息模板,要用commonNews核心
	var username = __mymvcCookies.get('Cookie_user');
	if(username != "" && $(".globalNavShow")){
		var strHtml = '您好！欢迎来到商务联盟！';
		strHtml +='<a target="_blank" href="'+global_member_url+'" class="login_sub hover">'+username+'</a>您好！';
        strHtml +='<a target="_self" title="退出登录" href="'+global_member_url+'login/loginout">【退出登录】</a>';
		$("#globalNavShow").html(strHtml);
	}
});
///加为收藏夹
function AddFavorite(sURL, sTitle)
{
	try{
		window.external.addFavorite(sURL, sTitle);
	}
	catch (e){
		try{
			window.sidebar.addPanel(sTitle, sURL, "");
		}
		catch (e){
			alert("添加收藏失败，请您按'Ctrl+D'手动添加！");
		}
	}
}
//头部搜索框js效果
function global_sel(target){
  var val    = $("[name='k']").val(); 
  if(target == "provide"){
	  $("#p").attr("class","sub_nav_sel");
	  $("#c").attr("class","");
	  $("#n").attr("class","");
	  $("#l").attr("class",""); 
	  if(val == "请输入关键字" | val == "请输入产品关键字" | val == "请输入关键字或公司名称" | val == "请输入关键字或资讯标题"){ 
	  $("[name='k']").val("请输入产品关键字");
	  $("[name='k']").attr("onfocus","if(this.value=='请输入产品关键字')this.value='';");

	  $("[name='k']").attr("onblur","if(this.value=='')this.value='请输入产品关键字';");  
	  }
  }else if(target == "company"){
	  $("#p").attr("class","");
	  $("#c").attr("class","sub_nav_sel");
	  $("#n").attr("class","");
	  $("#l").attr("class","");
	  if(val == "请输入关键字" | val == "请输入产品关键字" | val == "请输入关键字或公司名称" | val == "请输入关键字或资讯标题"){ 
	  
	  $("[name='k']").val("请输入关键字或公司名称");
	  $("[name='k']").attr("onfocus","if(this.value=='请输入关键字或公司名称')this.value='';");
	  $("[name='k']").attr("onblur","if(this.value=='')this.value='请输入关键字或公司名称';"); 
	  }  
  }else if(target == "news"){
	  $("#p").attr("class","");
	  $("#c").attr("class","");
	  $("#n").attr("class","sub_nav_sel");
	  $("#l").attr("class","");
	  if(val == "请输入关键字" | val == "请输入产品关键字" | val == "请输入关键字或公司名称" | val == "请输入关键字或资讯标题"){ 
	  
	  $("[name='k']").val("请输入关键字或资讯标题");
	  $("[name='k']").attr("onfocus","if(this.value=='请输入关键字或资讯标题')this.value='';");
	  $("[name='k']").attr("onblur","if(this.value=='')this.value='请输入关键字或资讯标题';"); 
	  } 
  }else if(target == "link"){
	  $("#p").attr("class","");
	  $("#c").attr("class","");
	  $("#n").attr("class","");
	  $("#l").attr("class","sub_nav_sel");
	  if(val == "请输入关键字" | val == "请输入产品关键字" | val == "请输入关键字或公司名称" | val == "请输入关键字或资讯标题"){  
	  $("[name='k']").val("请输入关键字或公司名称");
	  $("[name='k']").attr("onfocus","if(this.value=='请输入关键字或公司名称')this.value='';");
	  $("[name='k']").attr("onblur","if(this.value=='')this.value='请输入关键字或公司名称';"); 
	  }
  }
  var global_search_url = $("#global_search_url").val();
  var url = global_search_url + target + "_search.html"; 
  $("#global_search").attr("action",url);
} 
//头部搜索框提交效果 
function global_submit(){
	var val    = $("[name='k']").val();
	///默认说明或者空不能提交
	if(val == "" || val == "请输入关键字" || val == "请输入产品关键字" || val == "请输入关键字或公司名称" || val == "请输入关键字或资讯标题"){ 
		alert("请输入搜索的关键字");
		return false;
	}
	$("#global_search").submit();
}
