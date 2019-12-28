/*
	作者：叶华伟，邮箱：yhw2710@126.com,QQ:517025143
*/
$(function(){
			$(".news_content p:odd").addClass("p03");  //隔行换色处，额数行增加样式P03
			
			//鼠标经过样式变化处
			$(".news_content p").hover( 
                function () { 
                    $(this).addClass("p02");   //鼠标经过时增加样式P02
                }, 
                function () { 
                    $(this).removeClass("p02"); //鼠标离开时移除样式P02
                }
            )
			
			//超链接无虚线框处
			$("a").focus( 
                function () { 
                    $(this).blur(); //得到焦点与失去焦点效果一致
                }
             )
        })

//标题提示效果处
var sweetTitles = {
	x : 10,	
	y : 20,	
	tipElements : "a",
	init : function() {
		$(this.tipElements).mouseover(function(e){
			this.myTitle = this.title;
			this.myHref = this.href;
			this.myHref = (this.myHref.length > 200 ? this.myHref.toString().substring(0,200)+"..." : this.myHref);
			this.title = "";
			var tooltip = "";
			if(this.myTitle == "")
			{
			    tooltip = "";
			}
			else
			{
			    tooltip = "<div id='tooltip'><p>"+this.myTitle+"</p></div>";
			}
			$('body').append(tooltip);
			$('#tooltip')
				.css({
					"opacity":"1",
					"top":(e.pageY+20)+"px",
				"left":(e.pageX+10)+"px"
				}).show('fast');	
		}).mouseout(function(){
			this.title = this.myTitle;
			$('#tooltip').remove();
		}).mousemove(function(e){
			$('#tooltip')
			.css({
					"top":(e.pageY+20)+"px",
				"left":(e.pageX+10)+"px"
			});
		});
	}
};
$(function(){
	sweetTitles.init();
});