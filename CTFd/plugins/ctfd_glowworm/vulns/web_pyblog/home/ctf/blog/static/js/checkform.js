 function checkform()
{
     if($("#u_name").val()=="" || $("#u_name").val().length<2)
          {
              layer.msg('用户名不能为空或者昵称太短了喔', {icon: 2}); 
               return false;
          }

if($("#txaArticle").val()=="" || $("#txaArticle").val().length<2)
          {
              layer.msg('亲啥都没写喔，或者内容太少啦！', {icon: 2}); 
               return false;
          }
		  
		if($("#txaArticle").val()!="" && $("#u_name").val()!="")
          {
              layer.alert('恭喜提交成功！待管理员审核通过后显示!', {icon: 1}); 
               return true;
          }
		  
     else
     {
          return true;
     }
} 