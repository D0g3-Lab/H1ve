//公共提示窗口函数

var currentpage = "";
var pageSize = 6;
var pageIndex = 0;




$(function () {

    ///模版里面分页 修改 


    function PageCallback(index, jq) {

        InitTable(index);
    }

    //请求数据  
    function InitTable(pageIndex, typeTemple) {

        typeTemple = $("#getfreeORcharge").val();
        $.ajax({
            type: "POST",
            dataType: "text",
            url: '/Ajax_WebServer/Ajax_Templates.ashx',      //提交到一般处理程序请求数据  
            // url: '/pop/web/Ajax_Tempe/Ajax_Templates.ashx',      //提交到一般处理程序请求数据  
            data: "pageIndex=" + (pageIndex + 1) + "&pageSize=" + pageSize + "&ezsite_prd=" + typeTemple + "&type_code=1",          //提交两个参数：pageIndex(页面索引)，pageSize(显示条数)                  
            success: function (data) {
                if (data == "TimeOut") {
                    window.location.href = "/users/Login.aspx";
                }
                $("#choose_temple").empty();
                $("#choose_temple").append(data);

                $.ajax({
                    type: "POST",
                    dataType: "text",
                    url: '/Ajax_WebServer/Ajax_Templates.ashx',      //提交到一般处理程序请求数据  
                    data: "pageIndex=" + (pageIndex + 1) + "&pageSize=" + pageSize + "&ezsite_prd=" + typeTemple + "&type_code=2",          //提交两个参数：pageIndex(页面索引)，pageSize(显示条数)                  
                    success: function (result) {
                        //分页，PageCount是总条目数，这是必选参数，其它参数都是可选  
                        $("#Pagination").pagination(result, {
                            callback: PageCallback,
                            prev_text: ' ',       //上一页按钮里text  
                            next_text: ' ',       //下一页按钮里text  
                            items_per_page: pageSize,  //显示条数  
                            ellipse_text: '…',
                            num_display_entries: 6,    //连续分页主体部分分页条目数  
                            current_page: pageIndex,   //当前页索引  
                            num_edge_entries: 2        //两侧首尾分页条目数  
                        });

                    }
                });
            }
        });
    }
    ////////////////////////////修改与2011年10月26号 by jason



    $('.us_line').show();

    //-------------点击"编辑"按钮展开菜单条[start]--------code jason----------
    //    $('.sub_edit').bind('mouseenter', function () {
    //        $(this).css("background-position", "0px -120px");
    //    }).bind('mouseleave', function () {
    //        $(this).css("background-position", "0px -90px");
    //    });


    $('.sub_edit').click(function (event) {
        if ($(this).attr("href") == "javascript:void(0);") {

            return false;
        }

        var url = $(".us_line a").eq(0).attr("href");

        var name = $(this).parents().find(".tit h2").html();

        s_name = name.substring(0, name.indexOf('.'));
        if (s_name != "") {
            $.ajax({
                type: "POST",
                url: "/UserHome/Ajax_Server/Ajax_ForPhp_Session.ashx",
                data: "s_name=" + s_name,
                dataType: "html",
                async: true,
                success: function (response) {
                    if (response == "TimeOut") {
                        window.location.href = "/users/Login.aspx";
                    }
                },
                error: function (response) {
                    //  alert("err");
                }
            });

        }

        //        if ($(this).parent().parent().children('.us_line').css('display') == 'block')//如果已经有菜单，则点击按钮回收菜单
        //        {
        //            $(this).parent().parent().children('.us_line').slideUp('50');
        //            $(this).bind('mouseenter', function () {
        //                $(this).css("background-position", "0px -120px");
        //            }).bind('mouseleave', function () {
        //                $(this).css("background-position", "0px -90px");
        //            });

        //        }
        //        else//没有菜单，点击按钮展开菜单
        //        {
        //            $(this).parent().parent().children('.us_line').slideDown('100');
        //            $(this).css("background-position", "0px -120px").unbind('mouseenter').unbind('mouseleave');

        //        }
        event.stopPropagation();
    });
    //-------------点击"编辑"按钮展开菜单条[end]--------------------

    //-------------点击行展开菜单条[start]-------------------------
    $('.message_row').click(function () {
        if ($(this).find('.us_line').css('display') == 'block') {
            $(this).find('.us_line').slideUp('50');
            $(this).find('.sub_edit').bind('mouseenter', function () {
                $(this).css("background-position", "0px -120px");
            }).bind('mouseleave', function () {
                $(this).css("background-position", "0px -90px");
            }).css("background-position", "0px -90px");
        }
        else {
            $(this).find('.us_line').slideDown('100');
            $(this).find('.sub_edit').css("background-position", "0px -120px").unbind('mouseenter').unbind('mouseleave');
        }
    }).hover(function () {
        $(this).css('cursor', 'pointer');
    }, function () {
        $(this).css('cursor', 'default');
    });

    $('.message_row').find('.message_info,.sub_more').click(function (event) {
        event.stopPropagation();
    });

    $('.sub_more').hover(function () {
        $(this).children('.sub').show();
    }, function () {
        $(this).children('.sub').hide();
    });
    $(".sub").click(function () {
        $(this).hide();
    });


    //-------------分頁show[start]---------------code jason----------
    $(".us_page a:eq(0)").hover(
     function () {
         $(this).empty();

         $(this).append("<img src='/UserHome/images/left_w.gif'/>");
     },
   function () {
       $(this).empty();
       $(this).append("<img src='/UserHome/images/left_b.gif'/>");
   }
    );

    $(".us_page a:eq(1)").hover(
     function () {
         $(this).empty();

         $(this).append("<img src='/UserHome/images/right_w.gif'/>");
     },
   function () {
       $(this).empty();
       $(this).append("<img src='/UserHome/images/right_b.gif'/>");
   }
    );




    $(".dud_button1").live("click", function () {//花时间去分离了数组 了 不知道还有没有好点的办法。。。。

        var strx = $(this).attr("name");
        var obj = $(this).parent().parent();
        var objbutt = $(this);
        var index;
        var result_string = ""; //最终处理结果
        var arrss = new Array(); //把值放到数组里面
        $(".jasonchen").each(function (i) {
            arrss[i] = $(this).html();
        });
        if (arrss.length > 1) {//如果数组是2个以上的集合 做一下处理
            for (var i = 0; i < arrss.length; i++) {
                if (arrss[i] == strx) {
                    index = i;
                }
            }
            var oneofstring = (arrss[index]);
            var temparrs = arrss.join(',') + ','
            var arr = temparrs.replace(oneofstring + ',', '');
            var lastIndex = arr.lastIndexOf(',');
            result_string = arr.substring(0, lastIndex);
            // alert(result_string);

        } else if (arrss.length == 1) {

            result_string = arrss[0];
            //alert(result_string);
            result_string = "";
        }
        else {
            result_string = "";
        }

        if (true) {
            var pdtnme = $("#binddomainId").val();

            objbutt.empty();
            // objbutt.parent().append(msg.wating);
            objbutt.parent("td").html("...Deletting..."); //
            objbutt.hide();

            $.post("/UserHome/Ajax_Server/Ajax_All_V_ot51st.ashx", { pdtnme: pdtnme, result_string: result_string, typex: "2" }, function (jason) {
                if (jason == "10000") {
                    obj.remove();
                    ot5_rigth_ert(msg.delting, "1");
                } else if (jason == "TimeOut") {
                    window.location.href = "/users/Login.aspx";
                }
                else {
                    ot5alert(jason, 1);
                }

            }, "html");
        }
    });


    $(".working_close").hover(function () {//立即開通
        $(this).css('cursor', 'pointer');
        $(this).click(function () {
            window.location.href = "/pop/buy/cart.aspx";
        });
    });

    $(".tit").find("h1").click(function () {//如果运行状态为未开通 那么给个死连接


        if ($(this).parents(".titul_close").attr("title") == msgg.zhuangtaibuhao) {
            return false;
            $(this).parent("a").attr("href", "javascript:void(0);")
        }

    });
    //-------------点击"编辑"保存sesssingle[start]--------------------
    $(".us_line a span").click(function () {
        var name = $(this).parents().find(".tit h2").html();

        s_name = name.substring(0, name.indexOf('.'));
        if (s_name != "") {
            $.ajax({
                type: "POST",
                url: "/UserHome/Ajax_Server/Ajax_ForPhp_Session.ashx",
                data: "s_name=" + s_name,
                dataType: "html",
                async: true,
                success: function (response) {
                    if (response == "TimeOut") {
                        window.location.href = "/users/Login.aspx";
                    }

                },
                error: function (response) {
                    // alert("err");
                }
            });

        }
    });
    //-------------点击"编辑"保存sesssingle[end]--------------------working_normal


    //-------------点击非正常连接不然点[start]--------------------
    $(function () {

        if ($(".new_left .working_unusual").size() > 0) {
            $(".new_left .working_unusual").each(function () {
                $(this).parent(".info").next(".sub_more").next(".sub_edit").attr("href", "javascript:void(0);");
                $(this).parent(".info").next(".sub_more").find("ul li:eq(1)").find("a").attr("disabled", "disabled");
                if ($(this).prev().attr("class") == "update") {
                    $(this).prev(".update").attr("disabled", "disabled");
                }
                else {
                    // alert("11");
                }
            });
        }

        if ($(".new_left .working_close").size() > 0) {

            $(".new_left .working_close").each(function () {
                $(this).parent(".info").next(".sub_more").next(".sub_edit").attr("href", "javascript:void(0);");
                $(this).parent(".info").next(".sub_more").find("ul li:eq(1)").find("a").attr("disabled", "disabled");
                if ($(this).prev().attr("class") == "update") {
                    $(this).prev(".update").attr("disabled", "disabled");
                }
                else {
                    // alert("11");
                }
            });
        }

    });


    //-------------点击非正常连接不然点[end]--------------------


    $(".sub").each(function () {
        $(this).children("ul").children("li").eq(2).children("a").click(function () {
            delectweb($(this));
        });
        $(this).children("ul").children(" li").eq(0).children("a").click(function () {
            webinfo($(this)); //网站基本信息
        });
        $(this).children("ul").children(" li").eq(1).children("a").click(function () {

            binddomain($(this)); //域名绑定
        });
        //        $(this).children("ul").children(" li").eq(2).children("a").click(function () {
        //            upgrade($(this)); //升级
        //        });
        //        $(this).children("ul").children(" li").eq(3).children("a").click(function () {
        //            binddomain($(this)); //复制站点
        //        });
    });


    //  $("div.versions").each(function () {
    $(".update").click(function () {
        // alert($(this).parent(".info").next(".sub_more").find(".sub>ul").attr("id"));

        // return false;
        if ($(this).attr("disabled") == "disabled") {
            return false; //禁掉

        }
        upgrade($(this).parent(".info").next(".sub_more").find(".sub>ul").attr("id"));

    });
    //});
    $(".popclass").click(function () {
        if (($(this).attr("id") == "youcantopenfreenow") || ($(this).attr("id") == "youcantopenfreenowshop")) {
            //如果免费开通5个 限制
            ot5alert(mess.mostfive, "1");
            return false;
        }
        /* if ($(this).attr("id") == "freewebsite" || $(this).attr("id") == "freeshop") {
        $.ajax({
        type: "POST",
        url: '/Ajax_WebServer/Ajax_WebSite.ashx',
        data: { 'type_code': '3' },
        success: function (data) {
        if (data == "true") {
        */
        $("#getfreeORcharge").val($(this).attr("id"));  //标记是免费还是高级收费 
        $("#dialog-modal").dialog({
            // height: 332,
            width: 633,
            modal: true,
            resizable: false
        });
        /* } else {
        ot5alert(mess.mostfive, "1");
        }
        }
        });
        }*/
    });
    $("#Name_Next").click(function () {
        var ismpt = $("#Website_Name").val();
        var datacheck = $("#datacheck");
        if (ismpt == "") {
            datacheck.empty();
            datacheck.append("<img src='../../images/cross.png' />" + msg.notEmpty + "");
        }
        else {

            // var msg = "<%=gbl["gongxi"]%>";
            //  alert((msg));
            datacheck.empty();
            datacheck.append("<img src='../../images/tick.png' />" + msg.Congratulations + "");
            close_div();
            $("#Website_Domain").dialog({
                //  height: 623,
                width: 633,
                modal: true,
                resizable: false

            });

            $.post("/Ajax_WebServer/Ajax_get_dome.ashx", { 1: 1 }, function (results) {

                $("#comornet").empty();
                $("#comornet").append("<option>.com</option>");
                $("#comornet").append(results);
                $("#comornet option:eq(5)").remove();

            }, "html");
        }
    });

    $("#stepPerv").click(function () {//返回上一部
        $("#Website_Domain").dialog("close");
        $("#dialog-modal").dialog({
            // height: 332,
            width: 633,
            modal: true,
            resizable: false
        });

    });
    $("#temple_prev").live("click", function () {

        $("#choose_temple").dialog("close");
        $("#Website_Domain").dialog({
            //  height: 623,
            width: 633,
            modal: true,
            resizable: false

        });
    });



    $("#Website_Name").keydown(function (event) {

        if (event.keyCode == 13) {
            var ismpt = $("#Website_Name").val();
            var datacheck = $("#datacheck");
            if (ismpt == "") {
                datacheck.empty();
                datacheck.append("<img src='../../images/cross.png' />" + msg.notEmpty + "");
            }
            else {
                datacheck.empty();
                datacheck.append("<img src='../../images/tick.png' />" + msg.Congratulations + "");
                close_div();
                $("#Website_Domain").dialog({
                    //  height: 623,
                    width: 633,
                    modal: true,
                    resizable: false
                });
                $.post("/Ajax_WebServer/Ajax_get_dome.ashx", { 1: 1 }, function (results) {

                    $("#comornet").empty();
                    $("#comornet").append(results);

                }, "html");
            }
        }
    });



    $("input[name='yearss']").live('click', function () {
        //        if ($(this).attr("checked") == true) {
        //            $(this).parent("td").next("td").children("span").text($(this).val());
        //        }
        //        else if ($(this).attr("checked") == false) {
        //            $(this).parent("td").next("td").children("span").text("");
        //        }

    });

    $("#nextstep").click(function () {
        var New_Domain = $("#New_Domain").val();
        var Has_Domain_Msg = $("#Has_Domain_Msg");
        var chril_Domain = $("#chril_Domain").val();
        var comornet = $("#comornet").val();
        var ezsite_prd = $("#getfreeORcharge").val();
        var New_Domain_Msg = $("#New_Domain_Msg").text(); //错误提示chril_Domain_check
        if (New_Domain_Msg == msg.alerdreg) {
            $("#New_Domain").val(''); //如果註冊一個新域名 注册没通过 那么清空 
        }
        if (($("#chril_Domain").val() == "") && ($("#New_Domain").val() == "") && ($("#Has_Domain").val() == "")) {
            return;
        }
        if (($("#chril_Domain").val() == "") && ($("#Has_Domain").val() == "")) {

            if (New_Domain_Msg == msg.errsate) {
                return;
            }

        }
        if (($("#chril_Domain").val() == "") && ($("#New_Domain").val() == "")) {
            if (Has_Domain_Msg.text() != msg.pass) {
                return;
            }
        }
        if ($("#chril_Domain").val() == "") {
            $("#chril_Domain").val(makeid());
        }
        if ($("input[name='radio_button']:checked").val() == "2") {//第二個文本是選中的    msg.okreg  //"该域名异常!"//不正确的域名!
            if (New_Domain_Msg == msg.okreg) {//   该域名可以注册 即通过了二级域名又 通过了 新域名   該域名可以註冊   去域名表单那里吧 --------->>>>>> 該域名可以註冊！ 该域名异常！该域名可以注册！该域名已被注册  该域名异常!
                close_Website_Domain();
                $("#domian_from").dialog({
                    width: 845,
                    modal: true, //TODO:
                    resizable: false
                });
                $("#allprice2").html(New_Domain + comornet); //赋值给新域名的表单
                $.post("/UserHome/Ajax_Server/Ajax_Domian_From.ashx", { comornet: comornet }, function (result) {
                    if (result == "TimeOut") {
                        window.location.href = "/users/Login.aspx";
                    }
                    $("#reg_years").empty();
                    $("#reg_years").append(result);

                }, "html");
                //弹出的div的 show 出用户余额
                $.post("/UserHome/Ajax_Server/Ajax_getmemmny.ashx", { 1: 1 }, function (data) {
                    if (data == "TimeOut") {
                        window.location.href = "/users/Login.aspx";
                    }
                    $("#getmonytype").empty();
                    $("#getmonytype").append(data);
                }, "html");
            }

        }
        else if (($("input[name='radio_button']:checked").val() == "1") && ($("#chril_Domain_check").text() == msg.domereg)) {/////此二级域名可以注册!  domereg 直接去模版那里开通建站吧~
            close_Website_Domain();
            $("#Has_Domain").val("");
            $("#choose_temple").dialog({
                //  height: 730,
                width: 633,
                modal: true,
                resizable: false,
                position: [318, 177]
            });

            InitTable(0, ezsite_prd); /// 选模版
        }
        else if (($("input[name='radio_button']:checked").val() == "3") && ($("#Has_Domain_Msg").text() == msg.pass)) {//檢測通過

            close_Website_Domain();
            $("#choose_temple").dialog({
                //  height: 730,
                width: 633,
                modal: true,
                resizable: false,
                position: [318, 177]
            });

            InitTable(0, ezsite_prd); /// 选模版
        }
    });

    $("#chril_Domain,#New_Domain,#Has_Domain").keydown(function (event) {
        if (event.keyCode == 13) {
            var New_Domain = $("#New_Domain").val(); var Has_Domain_Msg = $("#Has_Domain_Msg");
            var chril_Domain = $("#chril_Domain").val(); var comornet = $("#comornet").val();
            var ezsite_prd = $("#getfreeORcharge").val();
            var New_Domain_Msg = $("#New_Domain_Msg").text(); //错误提示chril_Domain_check
            if (New_Domain_Msg == msg.alerdreg) {//该域名已被注册!
                $("#New_Domain").val(''); //如果註冊一個新域名 注册没通过 那么清空 
            }
            if (($("#chril_Domain").val() == "") && ($("#New_Domain").val() == "") && ($("#Has_Domain").val() == "")) {
                return;
            }
            if (($("#chril_Domain").val() == "") && ($("#Has_Domain").val() == "")) {

                if (New_Domain_Msg == msg.errsate) {//"该域名异常！"
                    return;
                }
            }
            if (($("#chril_Domain").val() == "") && ($("#New_Domain").val() == "")) {
                if (Has_Domain_Msg.text() != msg.pass) {//"檢測通過！"
                    return;
                }

            }

            if ($("#chril_Domain").val() == "") {
                $("#chril_Domain").val(makeid());
            }
            if ($("input[name='radio_button']:checked").val() == "2") {//第二個文本是選中的
                if (New_Domain_Msg == msg.okreg) {//該域名可以註冊！   即通过了二级域名又 通过了 新域名  去域名表单那里吧 --------->>>>>> 該域名可於註冊 该域名异常！该域名可以注册！该域名已被注册
                    close_Website_Domain();
                    $("#domian_from").dialog({
                        width: 845,
                        modal: true, //TODO:
                        resizable: false
                    });
                    $("#allprice2").html(New_Domain + comornet); //赋值给新域名的表单
                    $.post("/UserHome/Ajax_Server/Ajax_Domian_From.ashx", { comornet: comornet }, function (result) {
                        if (result == "TimeOut") {
                            window.location.href = "/users/Login.aspx";
                        }
                        $("#reg_years").empty();
                        $("#reg_years").append(result);
                    }, "html");
                    //弹出的div的 show 出用户余额
                    $.post("/UserHome/Ajax_Server/Ajax_getmemmny.ashx", { 1: 1 }, function (data) {
                        if (data == "TimeOut") {
                            window.location.href = "/users/Login.aspx";
                        }
                        $("#getmonytype").empty();
                        $("#getmonytype").append(data);
                    }, "html");
                }

            }
            else if (($("input[name='radio_button']:checked").val() == "1") && ($("#chril_Domain_check").text() == msg.domereg)) {//  此二级域名可以注册！///直接去模版那里开通建站吧~
                close_Website_Domain();
                $("#choose_temple").dialog({
                    //  height: 730,
                    width: 633,
                    modal: true,
                    resizable: false,
                    position: [318, 177]
                });
                InitTable(0, ezsite_prd); /// 选模版
            }
            else if (($("input[name='radio_button']:checked").val() == "3") && ($("#Has_Domain_Msg").text() == msg.pass)) {// "檢測通過！"

                close_Website_Domain();
                $("#choose_temple").dialog({
                    //  height: 730,
                    width: 633,
                    modal: true,
                    resizable: false,
                    position: [318, 177]
                });
                InitTable(0, ezsite_prd); /// 选模版
            }
        }

    });



    $("#upgrade_Jason").click(function () {

        var str = $("#User_Web_Info").attr("lang");
        //   alert(str);
        $("#User_Web_Info").dialog({
            width: 770,
            modal: true,
            resizable: false
        });
        $("#accordion").accordion({ autoHeight: false, active: 1 }); //升级服务
        var aaa = document.getElementById('Clear2');
        aaa.disabled = true; //使用true或false，控制是否让按钮禁用
        $.post("../../Ajax_WebServer/Ajax_UserSingle_Upgrade.ashx", { str: str }, function (upgrade) {
            if (upgrade == "TimeOut") {
                window.location.href = "/users/Login.aspx";
            } else {
                $("#upgrade").empty();
                $("#upgrade").append(upgrade);
                var aaa = document.getElementById('Clear2');
                aaa.disabled =false; //使用true或false，控制是否让按钮禁用
            }
        }, "html");
    });


    $("#webInfo_Jason").click(function () {
        var str = $("#User_Web_Info").attr("lang");
        $("#User_Web_Info").dialog({
            width: 770,
            modal: true,
            resizable: false
        });
        $("#accordion").accordion({ autoHeight: false, active: 0 }); //详细信息
        $.post("/Ajax_WebServer/Ajax_UserSingle_WebInfo.ashx", { str: str }, function (info) {
            $("#User_Web_Info").attr("lang", str);
            $("#webinfo").empty();
            $("#webinfo").append(info);
        }, "html");
    });

    $("#chril_Domain").focus(function () {
        jQuery("input[type='radio'][name='radio_button'][value='1']").attr("checked", "checked"); //此时value=1  表示选中
    });

    $("#chril_Domain").keyup(function () {//检查数据库是否已经存在此二级域名

        var s_nme = $("#chril_Domain").val();
        var chril_Domain_check = $("#chril_Domain_check")
        // jQuery("input[type='radio'][name='radio_button'][value='1']").attr("checked", "checked"); //此时value=1  表示选中
        var isornot = isDigit1(s_nme); //正则表达式检查是否否和要求
        if ((isornot == false) || (s_nme.length < 5)) {
            // $("#chril_Domain").val("");

            chril_Domain_check.empty();
            chril_Domain_check.append("<img src='../../../images/cross.png' id='imgsrc' />" + msg.zhuhe + ""); //5-16位字母或数字组合！
        }
        if (s_nme.length >= 5 && isornot == true) {
            chril_Domain_check.empty();
            chril_Domain_check.append("<img src='/images/xiaozhanggei.gif' />");
            $.post("/Ajax_WebServer/Ajax_Check_Data.ashx", { s_nme: s_nme }, function (data) {
                if (data == 0) {
                    chril_Domain_check.empty();
                    chril_Domain_check.append("<img src='../../../images/cross.png' id='imgsrc'/>" + msg.aldrdome + ""); //此二级域名已经存在请换一个！
                }
                else if (data == 1) {
                    chril_Domain_check.empty();
                    chril_Domain_check.append("<img src='../../../images/tick.png' />" + msg.domereg + ""); //此二级域名可以注册！
                } else if (data == "TimeOut") {
                    window.location.href = "/users/Login.aspx";
                }
            }, "html");
        }
    });
    $("#New_Domain").focus(function () {
        jQuery("input[type='radio'][name='radio_button'][value='2']").attr("checked", "checked"); //此时value=2 表示选中
        $("#New_Domain_Msg").empty();
    });
    $("#New_Domain").blur(function () {
        if ($(this).val().length == 0) {
            jQuery("input[type='radio'][name='radio_button'][value='2']").attr("checked", false); //此时value=2  表示选中
        }
    });
    $("#check_domain").click(function () {

        //  alert($("input[name='radio_button']:checked").val());
        var New_Domain = $("#New_Domain").val(); var comornet = $("#comornet").val(); var New_Domain_Msg = $("#New_Domain_Msg");
        if (New_Domain.length > 3) {
            New_Domain_Msg.empty();
            New_Domain_Msg.append("<img src='/images/xiaozhanggei.gif' />");
            $.ajax({
                type: "POST",
                url: "/Ajax_WebServer/Ajax_Check_NexDomain.ashx",
                data: "New_Domain=" + New_Domain + "&comornet=" + comornet + "&rdn=" + Math.random(),
                success: function (data) {
                    if (data == 0)
                    { New_Domain_Msg.empty(); New_Domain_Msg.append("<img src='../../../images/cross.png' id='imgsrc1' />" + msg.alerdreg + ""); } //该域名已被注册！
                    else if (data == 1)
                    { New_Domain_Msg.empty(); New_Domain_Msg.append("<img src='../../../images/tick.png' id='imgsrc9' />" + msg.okreg + ""); } //該域名可以註冊！
                    else if (data == 2) {
                        New_Domain_Msg.empty(); New_Domain_Msg.append("<img src='../../../images/cross.png' id='imgsrc1' />" + msg.errsate + ""); //该域名异常！
                    } else if (data == "TimeOut") {

                        window.location.href = "/users/Login.aspx";
                    }
                }
            });
        } else if (New_Domain.length == 0) {
            New_Domain_Msg.empty();
        }
    });

    $("#Has_Domain").focus(function () {
        jQuery("input[type='radio'][name='radio_button'][value='3']").attr("checked", "checked"); //此时value=3 表示选中
    });
    $("#Has_Domain").blur(function () {
        if ($(this).val().length == 0) {
            jQuery("input[type='radio'][name='radio_button'][value='3']").attr("checked", false); //此时value=3  表示选中
        }
    });

    $("#suerdiv").click(function () {
        $("#confrim").dialog("close");
        var chril_Domain = $("#chril_Domain").val(); //二级域名
        $.post("/Ajax_WebServer/Ajax_User_Pay_Rez.ashx", { chril_Domain: chril_Domain }, function (data) {
            if (data == 0) {

            }
            else {
                alert(data);
            }

        }, "html");

    });

    $("#Has_Domain").keyup(function () {
        var Has_Domain_Msg = $("#Has_Domain_Msg");

        if ($(this).val().length < 5) {
            Has_Domain_Msg.empty();
            Has_Domain_Msg.append("<img src='../../../images/cross.png' />" + msg.limdome + ""); //域名不低於4位有效字符！
        }
        else {
            if (isdomain($(this).val()) == false) {
                Has_Domain_Msg.empty();
                Has_Domain_Msg.append("<img src='../../../images/cross.png' />" + msg.plseas + ""); //請輸入正確的域名！
            }
            else {
                Has_Domain_Msg.empty();
                Has_Domain_Msg.append("<img src='../../../images/tick.png' />" + msg.pass + ""); //檢測通過！
            }
        }

    });

    //    $("#ot5_dme_new").click(function () {
    //        $(this).val("");
    //    });
    $("#sxss").live("click", function () {//域名绑定
        var ot5_dme_new = $("#ot5_dme_new").val();
        var free_or = $("#free_or").val();
        if (ot5_dme_new.length < 5) {
            $("#ot5_dme_new").val("");
            return false;
        }

        if (isdomain(ot5_dme_new) == false) {
            ot5alert(msg.plseas, "1"); //請輸入正確的域名！
            $("#ot5_dme_new").val("");
            return false;
        }
        if (free_or == "1") {
            var times = ot5_dme_new.split(',').length;
            if ($("table.us_table1 .jasonchen").size() > 0) {///判读 是否存在一个域名了
                ot5alert(msg.isorry, "1"); //對不起！您只能綁定一個域名，趕快升級吧！可以綁定多個域名！
                $("#ot5_dme_new").val("");
                return false;

            }

            if (times > 1) {
                ot5alert(msg.stailing, "1"); //您只能綁定一個域名！
                $("#ot5_dme_new").val("");
                return false;
            }
        }
        if (free_or == "10") {
            var times = ot5_dme_new.split(',').length;
            if (times >= 10) {
                ot5alert(msg.ybind, "1"); //您只能綁定10個域名！
                $("#ot5_dme_new").val("");
                return false;
            }
        }
        var items = "";
        var times = "";
        $(".jasonchen").each(function (i) {
            items += ($(this).html()) + ",";
        });
        times = $(".jasonchen").size();
        if (times >= 10) {
            ot5alert(msg.ybind, "1"); //您只能綁定10個域名！
            $("#ot5_dme_new").val("");
            return false;
        }

        var str = $("#binddomainId").val(); //网站名称
        var domians = $("#ot5_dme_new").val(); //输入的域名

        if (str != "" && domians != "") {
            var domian = (items + domians);
            $("#loading_div").show(); //加载中
            $("#binddime").dialog("close"); //影藏绑定输入div

            $.post("/Ajax_WebServer/Ajax_UserSingle_binddomain.ashx", { str: str, domian: domian }, function (upgrade) {
                
                if (upgrade == "TimeOut") {
                    window.location.href = "/users/Login.aspx";
                } else {
                    $("#loading_div").hide(); //加载完成
                    if (upgrade == "1") {
                        ot5alert(msg.conts, "1"); //含有特殊字符！
                    }
                    else if (upgrade == "0") {

                        ot5_rigth_ert(msg.binding, "1"); //恭喜，綁定成功！
                    }
                    else {
                      
                        ot5alert(upgrade, "1");
                    }
                }

            }, "html");
        }
    });


    $("#vipwebsite").click(function () {//xjd test
        var str = "1";
        var Website_Name = "vip" + makeid();
        var chril_Domain = "vip" + makeid();
        var ezsite_prd = "vipwebsite";
        var years = "1";
        $("#loading").dialog({
            height: 95,
            width: 518,
            modal: true,
            resizable: false
        });

        $.post("/Ajax_WebServer/Ajax_User_Order.ashx", { template_id: str, Website_Name: Website_Name, chril_Domain: chril_Domain, ezsite_prd: ezsite_prd, years: years }, function (jason) {
            if (jason == 0) {
                self.location = "/pop/buy/cart.aspx";
            }
            else {
                alert(jason);
            }
        }, "html");
    });


    $("btn_sure").click(function () {
        alert("111");
    });

    $("#backdiv").click(function () {
        $("#choose_temple").dialog({
            width: 800,
            modal: true,
            resizable: false
        });


    });

    /////////////9-26 修改


    $("#canle").click(function () {//取消
        $("#yes_or").dialog("close");
    });
    $("#canle2").click(function () {//取消2
        $("#yes_or2").dialog("close");
    });

    $("#cancleagan").click(function () {

        $("#deletwebagian").dialog("close");
    });


    $("#canle").click(function () {//取消   
        $("#yes_or").dialog("close");
    });


    $("#sure.us_ok").click(function (i) {//确定
        var str = $("#hostname").val();
        var newproid = $(".g_prdtype").val();
        $("#yes_or").dialog("close");
        var yeaer = $("input:radio[name='yearss'][checked]").next("span").text();
        // var tmetpe = $("input:radio[name='yearss'][checked]").next("span").next("span").text();
        // alert(tmetpe);
        var tmetpe = $("input:radio[name='yearss'][checked]").next("span").next("span").next("input").val();
        var Real_value = $("input:radio[name='yearss'][checked]").parent("td").next("td").children("span").text(); //选中产品的价值。
        if (str.length > 0 && newproid.length > 0) {
            $.post("/Ajax_WebServer/Ajax_UserSingle_Upgrade_Ing.ashx", { str: str, yeaer: yeaer, newproid: newproid, tmetpe: tmetpe, Real_value: Real_value }, function (data) {
                if (data == "TimeOut") {
                    window.location.href = "/users/Login.aspx";
                } else {
                    if (data == "10000") {
                        ot5_rigth_ert(msg.congr_grd, "1"); //恭喜您！升級成功！
                        location.reload();
                    }
                    else if (data.substring(0, 5) == "50000") {
                        self.location = "/UserHome/ot5lst/payupgrade/payupgrade.aspx?" + data;
                    }
                    else {
                        ot5alert(data, 1);

                    }
                }
            }, "html");
        }
    });




    //////////

    //10-11日修改//1360

    $("#delagan").click(function () {
        $("#deletwebagian").dialog("close");

        $("#yes_or2").dialog({
            height: 126,
            width: 350,
            modal: true,
            resizable: false
        });
    });


    $("#sure2").click(function () {//确定
        var xx = window.location.search;
        var yy = (xx.substring(1, xx.length));
        var zz = obj.find(".jason").val(); //1 表示正常
        var uu = obj.find(".chen").val();
        $("#yes_or2").dialog("close"); //关闭询问
        $("#loading_div").show(); //加载中
        $.ajax({
            url: 'deleteWeb.aspx',
            async: true,
            cache: false,
            data: 's_nme=' + str + '&' + yy + '&state=' + zz + '&webpage=' + uu,
            success: function (data) {
                if (data == "TimeOut") {
                    window.location.href = "/users/Login.aspx";
                }
                $("#loading_div").hide(); //加载完成
                if (data.split('||')[0] == "typeone") {
                    window.location.href = data.split('||')[1];
                }
                else if (data.split('||')[0] == "typetwo") {
                    ot5alert(data.split('||')[1].split('|')[0], data.split('||')[1].split('|')[1]);
                }
            }
        });
        //window.location.href = "../ot5lst/deleteWeb.aspx?s_nme=" + str + "&" + yy + "&state=" + zz + "&webpage=" + uu;

    });


});

function close_div() {
    $("#dialog-modal").dialog("close");
    // alert($(this).attr("id"));

}
function close_Website_Domain() {
    $("#Website_Domain").dialog("close");
}
function gosoye(str) {//首页
    var ezsite_prd = $("#getfreeORcharge").val();
    $.post("/Ajax_WebServer/Ajax_Templates.ashx", { ezsite_prd: ezsite_prd, rquestpage: str }, function (data) {
        //        if (data == "TimeOut") {
        //            window.location.href = "/users/Login.aspx";
        //        }
        $("#choose_temple").empty();
        $("#choose_temple").append(data);
    }, "html");

}
function goPage_N() {//下一页
    var str = $("#count").text()
    var ezsite_prd = $("#getfreeORcharge").val();
    str++;
    $.post("/Ajax_WebServer/Ajax_Templates.ashx", { ezsite_prd: ezsite_prd, rquestpage: str }, function (data) {
        //        if (data == "TimeOut") {
        //            window.location.href = "/users/Login.aspx";
        //        }
        $("#choose_temple").empty();
        $("#choose_temple").append(data);
    }, "html");
}
function goPage_P() {//上一页
    var str = $("#count").text();
    var ezsite_prd = $("#getfreeORcharge").val();
    str--;
    $.post("/Ajax_WebServer/Ajax_Templates.ashx", { ezsite_prd: ezsite_prd, rquestpage: str }, function (data) {
        //        if (data == "TimeOut") {
        //            window.location.href = "/users/Login.aspx";
        //        }
        $("#choose_temple").empty();
        $("#choose_temple").append(data);
    }, "html");

}
function postdata(str) {// code by  jason
    $("#choose_temple").dialog("close");
    $("#loading").dialog({
        height: 95,
        width: 518,
        modal: true,
        resizable: false
    });
    var template_id = str           //模板的id
    var Website_Name = $("#Website_Name").val(); //网站标题
    var chril_Domain = $("#chril_Domain").val(); //二级域名
    var New_Domain = $("#New_Domain").val(); //新域名
    var comornet = $("#comornet").val(); //后缀 .com ,.net
    var Has_Domain = $("#Has_Domain").val(); //已有域名
    //  var ezsite_prd = "jzmf100_1007";
    var ezsite_prd = $("#getfreeORcharge").val();  //获取 隐藏的id
    if (ezsite_prd == "deluxewebsite") {
        var years = $("input[name='website']:checked").val();
    } else {
        var years = $("input[name='shop']:checked").val();
    }
    if (years == "" || years == undefined) {
        years = "1";
    }

    // alert(ezsite_prd);
    if ((ezsite_prd != "") && (ezsite_prd != "freewebsite") && (ezsite_prd != "freeshop")) {//高级版   因为这是非免费版
        $.post("/Ajax_WebServer/Ajax_User_Order.ashx", { template_id: str, Website_Name: Website_Name, chril_Domain: chril_Domain, New_Domain: New_Domain, Has_Domain: Has_Domain, ezsite_prd: ezsite_prd, years: years }, function (jason) {
            if (jason == 0) {//表示订单成功

                //   if (New_Domain.length > 0 && Has_Domain.length > 0) {//新域名不为空并且 已有域名也不为空
                //      $.post("/Ajax_WebServer/Ajax_UserSingle_binddomain.ashx", { domian: New_Domain + comornet + "," + Has_Domain, str: chril_Domain }, function (json) {//第三部 绑定域名

                ///一個開通建站結束後清空的項目
                $("#Website_Name").val(""); //网站标题
                $("#chril_Domain").val(""); //二级域名
                $("#New_Domain").val(""); //新域名
                $("#Has_Domain").val(""); //已有域名
                $("#datacheck").empty(); //是否通過
                $("#chril_Domain_check").empty(); //是否可以註冊
                $("#New_Domain_Msg").empty(); //已有的域名
                $("#loading").dialog("close");
                // ot5alert(msg.ording, "1"); //訂單已經生成，三秒钟後自動跳轉到結算頁面
                // setTimeout("self.location='/pop/buy/cart.aspx'", 3000);
                self.location = "/pop/buy/cart.aspx";

                //  });
                //  }

            }
            else if (jason = "NoSeesion") {// ot5alert(msg.NoSeesion, "1"); //登录超时


                //  ot5alert(msg.NoSeesion, "1"); //登录超时
                self.location = "/users/Login.aspx";
            } else {
                ///一個開通建站結束後清空的項目
                $("#Website_Name").val(""); //网站标题
                $("#chril_Domain").val(""); //二级域名
                $("#New_Domain").val(""); //新域名
                $("#Has_Domain").val(""); //已有域名
                $("#datacheck").empty(); //是否通過
                $("#chril_Domain_check").empty(); //是否可以註冊
                $("#New_Domain_Msg").empty(); //已有的域名
                $("#loading").dialog("close");
                ot5alert(jason, "1"); //提示框
            }
        }, "html");


    }
    else {// 免費版本
        $.post("/Ajax_WebServer/Ajax_User_Order.ashx", { template_id: str, Website_Name: Website_Name, chril_Domain: chril_Domain, New_Domain: New_Domain, Has_Domain: Has_Domain, ezsite_prd: ezsite_prd }, function (data) {
            if (data == 0) {//表示订单成功
                $.post("/Ajax_WebServer/Ajax_User_Pay_Rez.ashx", { chril_Domain: chril_Domain }, function (result) {
                    if (result == 0) { //表示购买、开通啦！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
                        if (New_Domain.length > 0 && Has_Domain.length > 0) {//新域名不为空并且 已有域名也不为空
                            $.post("/Ajax_WebServer/Ajax_UserSingle_binddomain.ashx", { domian: New_Domain + comornet + "," + Has_Domain, str: chril_Domain }, function (json) {//第三部 绑定域名
                                if (json == "TimeOut") {
                                    window.location.href = "/users/Login.aspx";
                                } else {
                                    if (json == 0)//绑定成功
                                    {
                                        ///一個開通建站結束後清空的項目
                                        $("#Website_Name").val(""); //网站标题
                                        $("#chril_Domain").val(""); //二级域名
                                        $("#New_Domain").val(""); //新域名
                                        $("#Has_Domain").val(""); //已有域名
                                        $("#datacheck").empty(); //是否通過
                                        $("#chril_Domain_check").empty(); //是否可以註冊
                                        $("#New_Domain_Msg").empty(); //已有的域名
                                        $("#loading").dialog("close");
                                        // window.location.href = "../../UserHome/ot5lst/main.aspx?s_nme=" + chril_Domain;
                                        if (ezsite_prd == "freeshop") {
                                            window.location.href = "/UserHome/ot5lst/webshop.aspx";
                                        } else {
                                            window.location.href = "/UserHome/ot5lst/website.aspx";
                                        }
                                    }
                                    else//绑定不成功
                                    {
                                        ///一個開通建站結束後清空的項目
                                        $("#Website_Name").val(""); //网站标题
                                        $("#chril_Domain").val(""); //二级域名
                                        $("#New_Domain").val(""); //新域名
                                        $("#Has_Domain").val(""); //已有域名
                                        $("#datacheck").empty(); //是否通過
                                        $("#chril_Domain_check").empty(); //是否可以註冊
                                        $("#New_Domain_Msg").empty(); //已有的域名
                                        $("#loading").dialog("close");
                                        ot5alert(json, "1");
                                    }
                                }
                            }, "html");
                        } else if (New_Domain.length == 0 && Has_Domain.length > 0) { //表示 没有新域名 但是有现有的域名
                            $.post("/Ajax_WebServer/Ajax_UserSingle_binddomain.ashx", { domian: Has_Domain, str: chril_Domain }, function (json) {//第三部 绑定域名
                                if (json == "TimeOut") {
                                    window.location.href = "/users/Login.aspx";
                                } else {
                                    if (json == 0)//绑定成功
                                    {
                                        ///一個開通建站結束後清空的項目
                                        $("#Website_Name").val(""); //网站标题
                                        $("#chril_Domain").val(""); //二级域名
                                        $("#New_Domain").val(""); //新域名
                                        $("#Has_Domain").val(""); //已有域名
                                        $("#datacheck").empty(); //是否通過
                                        $("#chril_Domain_check").empty(); //是否可以註冊
                                        $("#New_Domain_Msg").empty(); //已有的域名
                                        $("#loading").dialog("close");
                                        if (ezsite_prd == "freeshop") {
                                            window.location.href = "/UserHome/ot5lst/webshop.aspx";
                                        } else {
                                            window.location.href = "/UserHome/ot5lst/website.aspx";
                                        }

                                    }
                                    else//绑定不成功
                                    {
                                        ///一個開通建站結束後清空的項目
                                        $("#Website_Name").val(""); //网站标题
                                        $("#chril_Domain").val(""); //二级域名
                                        $("#New_Domain").val(""); //新域名
                                        $("#Has_Domain").val(""); //已有域名
                                        $("#datacheck").empty(); //是否通過
                                        $("#chril_Domain_check").empty(); //是否可以註冊
                                        $("#New_Domain_Msg").empty(); //已有的域名
                                        $("#loading").dialog("close");
                                        ot5alert(json, "1");
                                    }
                                }
                            }, "html");
                        } else if (New_Domain.length > 0 && Has_Domain.length == 0) {//表示 有新域名 但是没有现有的域名
                            $.post("/Ajax_WebServer/Ajax_UserSingle_binddomain.ashx", { domian: New_Domain + comornet, str: chril_Domain }, function (json) {//第三部 绑定域名
                                if (json == "TimeOut") {
                                    window.location.href = "/users/Login.aspx";
                                } else {
                                    if (json == 0)//绑定成功
                                    {
                                        ///一個開通建站結束後清空的項目
                                        $("#Website_Name").val(""); //网站标题
                                        $("#chril_Domain").val(""); //二级域名
                                        $("#New_Domain").val(""); //新域名
                                        $("#Has_Domain").val(""); //已有域名
                                        $("#datacheck").empty(); //是否通過
                                        $("#chril_Domain_check").empty(); //是否可以註冊
                                        $("#New_Domain_Msg").empty(); //已有的域名
                                        $("#loading").dialog("close");
                                        // window.location.href = "../../UserHome/ot5lst/main.aspx?s_nme=" + chril_Domain;
                                        if (ezsite_prd == "freeshop") {
                                            window.location.href = "/UserHome/ot5lst/webshop.aspx";
                                        } else {
                                            window.location.href = "/UserHome/ot5lst/website.aspx";
                                        }
                                    }
                                    else//绑定不成功
                                    {
                                        ///一個開通建站結束後清空的項目
                                        $("#Website_Name").val(""); //网站标题
                                        $("#chril_Domain").val(""); //二级域名
                                        $("#New_Domain").val(""); //新域名
                                        $("#Has_Domain").val(""); //已有域名
                                        $("#datacheck").empty(); //是否通過
                                        $("#chril_Domain_check").empty(); //是否可以註冊
                                        $("#New_Domain_Msg").empty(); //已有的域名
                                        $("#loading").dialog("close");

                                        ot5alert(json, "1");
                                    }
                                }
                            }, "html");
                        }
                        else {
                            ///一個開通建站結束後清空的項目
                            $("#Website_Name").val(""); //网站标题
                            $("#chril_Domain").val(""); //二级域名
                            $("#New_Domain").val(""); //新域名
                            $("#Has_Domain").val(""); //已有域名
                            $("#datacheck").empty(); //是否通過
                            $("#chril_Domain_check").empty(); //是否可以註冊
                            $("#New_Domain_Msg").empty(); //已有的域名
                            //只有使用Wopop.com的子域名
                            $("#loading").dialog("close");
                            // window.location.href = "../../UserHome/ot5lst/main.aspx?s_nme=" + chril_Domain;
                            if (ezsite_prd == "freeshop") {
                                window.location.href = "/UserHome/ot5lst/webshop.aspx";
                            } else {
                                window.location.href = "/UserHome/ot5lst/website.aspx";
                            }
                        }
                    }
                    else {
                        ///一個開通建站結束後清空的項目
                        $("#Website_Name").val(""); //网站标题
                        $("#chril_Domain").val(""); //二级域名
                        $("#New_Domain").val(""); //新域名
                        $("#Has_Domain").val(""); //已有域名
                        $("#datacheck").empty(); //是否通過
                        $("#chril_Domain_check").empty(); //是否可以註冊
                        $("#New_Domain_Msg").empty(); //已有的域名
                        //开通不成功！
                        $("#loading").dialog("close");
                        ot5alert(result, "1");
                    }
                }, "html");
            }
            else if (data = "NoSeesion") { // ot5alert(msg.NoSeesion, "1"); //登录超时

                self.location = "/users/Login.aspx";
            }
            else {//订单不成功
                ///一個開通建站結束後清空的項目
                $("#Website_Name").val(""); //网站标题
                $("#chril_Domain").val(""); //二级域名
                $("#New_Domain").val(""); //新域名
                $("#Has_Domain").val(""); //已有域名
                $("#datacheck").empty(); //是否通過
                $("#chril_Domain_check").empty(); //是否可以註冊二級域名
                $("#New_Domain_Msg").empty(); //已有的域名
                $("#loading").dialog("close");
                ot5alert(data, "1");
            }

        }, "html");
    }
}

function isdomain(str) {

    // var reg = /^([a-zA-Z0-9-]+\.)+(com|cn|net|biz|name|info|tv|org|cc|hk|mobi|name|asia|ws|us|mn|bz|in|me)$/;
    var reg = /([\S\s]+\.)+(com|cn|net|biz|name|tw|info|tv|org|cc|hk|mobi|asia|co|so|ws|us|mn|bz|in|me|中国|公司|网络)$/;
    var regg = /[\>@#\$%\^&\*)!(~<|。=?+\\\;；\、\/\{\}\[\]:：\'\"\“！……￥ `·]+/g;
    if (str.toLowerCase().indexOf("http://") == 0) {
        return false;
    }
    else if (!reg.test(str)) {
        return false;
    }
    else if (regg.test(str)) {
        return false;
    }
    else {

        return true;
    }
}


function isDigit1(str) {
    var reg = /^[a-zA-Z0-9\\-]{4,16}$/;    //  现在的  ^[a-zA-Z0-9\\-]{4,16}$   这个是原来的  /^[a-zA-Z0-9\\-_]{4,16}$/;
    return reg.test(str);
    //   if (str.length < 5)
    //   {return false;}
    //   if (!re.exec(str))
    //   { return false; }

    //  var reg = /^[a-zA-Z]{1}([a-zA-Z0-9]|[._]){4,16}$/;
    //  if (!reg.exec(str)) return false
    //  return true 
}
function regcheck(pattern, obj, errInfos) {//z输入中文域名
    if (pattern.test(obj.value)) {
        alert(errInfos);
        obj.focus();
        return false;
    }
    return true;
}
function price() {
    var yesars = $("#years").val();
    var prohg = $("#p_prohg").val();
    $("#years").val(yesars * prohg);
}

function delectweb(obj) {//删除网站实体
    window.obj = obj;
    window.str = obj.parent("li").parent("ul").attr("id");
    $("#deletwebagian").dialog({
        height: 126,
        width: 350,
        modal: true,
        resizable: false
    });
    $("#showmsg").html(msg.ysure); //您確認要刪除 " + str + ".wopop.com 這個站點麼？
//    $("#delagan").click(function () {
//        $("#deletwebagian").dialog("close");

//        $("#yes_or2").dialog({
//            height: 126,
//            width: 350,
//            modal: true,
//            resizable: false
//        });

        //     var str = obj.parent("li").parent("ul").attr("id");
        // var state = str.parent("div").parent("li").parent("div").attr("class");
//        $("#sure2").click(function () {//确定
//            // var str = location.href;
//            var xx = window.location.search;
//            var yy = (xx.substring(1, xx.length));
//            var zz = obj.find(".jason").val(); //1 表示正常
//            var uu = obj.find(".chen").val();
//            $("#yes_or2").dialog("close"); //关闭询问
//            $("#loading_div").show(); //加载中
//            $.ajax({
//                url: 'deleteWeb.aspx',
//                async: true,
//                cache: false,
//                data: 's_nme=' + str + '&' + yy + '&state=' + zz + '&webpage=' + uu,
//                success: function (data) {
//                    if (data == "TimeOut") {
//                        window.location.href = "/users/Login.aspx";
//                    }
//                    $("#loading_div").hide(); //加载完成
//                    if (data.split('||')[0] == "typeone") {
//                        window.location.href = data.split('||')[1];
//                    }
//                    else if (data.split('||')[0] == "typetwo") {
//                        ot5alert(data.split('||')[1].split('|')[0], data.split('||')[1].split('|')[1]);
//                    }
//                }
//            });
//            //window.location.href = "../ot5lst/deleteWeb.aspx?s_nme=" + str + "&" + yy + "&state=" + zz + "&webpage=" + uu;

//        });


  //  });



}

function webinfo(obj) {
    $("#webinfo").dialog({
        width: 770,
        modal: true,
        resizable: false
      //  position:[100,200]
    });
    //   $("#accordion").accordion({ autoHeight: false, active: 0 });  //基本信息
    var str = obj.parent("li").parent("ul").attr("id");
    $.post("/Ajax_WebServer/Ajax_UserSingle_WebInfo.ashx", { str: str }, function (info) {
        if (info == "TimeOut") {
            window.location.href = "/users/Login.aspx";
        } else {
            $("#webinfo").empty();
            $("#webinfo").append(info);
        }
    }, "html");


}
///域名列表
function binddomain(obj) {
    if (obj.attr("disabled") == "disabled") {

        return false; //异常禁掉
    }
    var str = obj.parent("li").parent("ul").attr("id");
    $("#binddime").dialog({
        width: 600,
        // height:305,
        modal: true,
        resizable: false
    });
    //绑定域名列表
    if (str != "") {
        var tobdy = "<table class='us_table1' width='100%' cellspacing=\"2\" cellpadding=\"0\" border=\"0\" >";
        tobdy += "<tr bgcolor=\"#D7EDFF\"><td height=\"22\" colspan=\"3\" class=txtcolor><div align=center><b>" + msg.bingdomess + "</font></b></div></td></tr>";
        $.post("/UserHome/Ajax_Server/Ajax_All_V_ot51st.ashx", { str: str, typex: "1" }, function (jason) {
            if (jason == "1") {
                $("#domeList").empty();
                $("#domeList").append(msg.sorrys); //對不起！您暫時還沒有域名！請自行添加。
            } else if (jason == "TimeOut") {
                window.location.href = "/users/Login.aspx";
            }
            else {
                $.each(jason.jsonstr, function (i, vale) {
                    if (vale.s_o3.split(",") == "") {
                        $("#domeList").empty();
                        $("#domeList").append(msg.sorrys); //"對不起！您暫時還沒有域名！請自行添加。"
                    }
                    else {
                        for (var j = 0; j < vale.s_o3.split(",").length; j++) {
                            tobdy += " <tr align=\"middle\" bgcolor=\"#ffffff\"><td width=\"25%\" height=\"22\"><p align=\"center\">" + (j + 1) + "</td><td class=\"jasonchen\" width=\"55%\">" + vale.s_o3.split(",")[j] + "</td> <td width=\"20%\" align=left> <input type=submit  name=" + vale.s_o3.split(",")[j] + " class='dud_button1 allsub' value=\"　" + msg.delebindname + "　\"> </td></tr>";
                        }
                    }
                    if (vale.g_prd == "freewebsite" || vale.g_prd == "freeshop")//此处赋值给ot5_dme_new  看看 是免费还是高级版本 以便判断1 还是10个域名绑定
                    {
                       /// $("#ot5_dme_new").val(msg.stailing); //您可以綁定1個域名！
                        $("#free_or").val("1"); //綁定一個域名
                    } else {

                     ///   $("#ot5_dme_new").val(msg.ycanb); //"您可以綁定1到10個域名！"
                        $("#free_or").val("10"); //可以10個域名
                    }

                });
                tobdy += "</table>";
                $("#domeList").empty();
                $("#domeList").append(tobdy);

            }

        }, "json");

    }

    $("#binddomainId").attr("value", str); //误删


}
function upgrade(obj) {
    var str = obj;
    var thispage = document.URL;
    var comfrompage;
    if (thispage.indexOf('UserHome/ot5lst/website.aspx') == -1) {
        comfrompage = "deluxeshop";
    }
    else {
        comfrompage = "deluxewebsite";
    }
    window.location.href = "/userhome/ot5lst/upgrade.aspx?str=" + str + "&comfrompage=" + comfrompage;
    //第三次修改 我不信还会变回去了？？？
//    $("#upgrade").dialog({
//        width: 770,
//        modal: true,
//        resizable: false
//    });
//    // $("#accordion").accordion({ autoHeight: false, active: 1 }); //升级服务
//    $.post("/Ajax_WebServer/Ajax_UserSingle_Upgrade.ashx", { str: str, comfrompage: comfrompage }, function (upgrade) {
//        if (upgrade == "TimeOut") {
//            window.location.href = "/users/Login.aspx";
//        } else {
//            $("#upgrade").empty();
//            $("#upgrade").append(upgrade);
//        }

//    }, "html");
}
///随机8位数
function makeid() { var text = "pop"; var possible = "abcdefghijklmnopqrestuvwxyz12456789"; for (var i = 0; i < 9; i++) text += possible.charAt(Math.floor(Math.random() * possible.length)); return text; }


function upfree() {//升级按钮


    if ($("input:radio[name='yearss'][checked]").val() == null) {//没选的情况下
        ot5alert(msg.choose, "1"); //要选择其中一项年份

    } else {

        $("#askformessage").empty();
        $("#askformessage").html(msg.aresuer); //如果確认升级空间型号，系統将自动扣除您的款項？
        $("#yes_or").dialog({
            height: 126,
            width: 350,
            modal: true,
            resizable: false
        });


    }
}

///根據操作系統或者瀏覽器的語言版本跳轉不同的 版本頁面
function chooseretun() {
    var type = navigator.appName
    if (type == "Netscape") {
        var lang = navigator.language
    }
    else {
        var lang = navigator.userLanguage
    }
    //取得国家代码的前两个字母  
    var lang = lang.substr(0, 2)
    // 英语  
    if (lang == "en") {
        // window.location.href = "http://www.une-system.com.cn/"
    }
    // 中文 - 不分繁体和简体  
    else if (lang == "zh") {
        //  window.location.href="http://www.une-system.com/"  
        //  注释掉了上面跳转,不然会陷入无限循环  
    }
    // 除上面所列的语言  
    else {
        //  window.location.href = "http://www.une-system.com.cn/"
    }
}


function ot5alert(mess, type) {
    $("#alertmessage").html(mess);
    $("#all_err_msg").dialog({
        resizable: false,
        height: 128,
        width: 350,
        modal: true
    });

    $("#alertok").click(function () {
        if (type == "1") {//点击确定只需要关闭
            $("#all_err_msg").dialog("close");
        }
        else if (type == "2") {//点击确定关闭层 然后跳转 
            $("#all_err_msg").dialog("close");
            window.location.href = "/pop/buy/cart.aspx";
        }
        else {
            $("#all_err_msg").dialog("close");
            window.location.href = type;
        }
    });
}

function ot5_rigth_ert(mess, type) {
    $("#alert_right_message").html(mess);
    $("#all_rigtht").dialog({
        resizable: false,
        // height: 126,
        width: 350,
        modal: true
    });

    $("#alertok_mesg").click(function () {
        var ezsite_prd = $("#getfreeORcharge").val();
        if (type == "1") {//點擊關閉
            $("#all_rigtht").dialog("close");
        }
        else if (type == "2") { //等待命令
            $("#all_rigtht").dialog("close");


            InitTables(0, ezsite_prd); /// 选模版
           



        }
    });
}

///////////////
function PageCallback(index, jq) {

    InitTables(index);
}

//请求数据  
function InitTables(pageIndex, typeTemple) {
    alert("ok");
    typeTemple = $("#getfreeORcharge").val();
    $.ajax({
        type: "POST",
        dataType: "text",
        url: '/Ajax_WebServer/Ajax_Templates.ashx',      //提交到一般处理程序请求数据  
        // url: '/pop/web/Ajax_Tempe/Ajax_Templates.ashx',      //提交到一般处理程序请求数据  
        data: "pageIndex=" + (pageIndex + 1) + "&pageSize=" + pageSize + "&ezsite_prd=" + typeTemple + "&type_code=1",          //提交两个参数：pageIndex(页面索引)，pageSize(显示条数)                  
        success: function (data) {
            if (data == "TimeOut") {
                window.location.href = "/users/Login.aspx";
            }
            $("#choose_temple").empty();
            $("#choose_temple").append(data);

            $.ajax({
                type: "POST",
                dataType: "text",
                url: '/Ajax_WebServer/Ajax_Templates.ashx',      //提交到一般处理程序请求数据  
                data: "pageIndex=" + (pageIndex + 1) + "&pageSize=" + pageSize + "&ezsite_prd=" + typeTemple + "&type_code=2",          //提交两个参数：pageIndex(页面索引)，pageSize(显示条数)                  
                success: function (result) {
                    //分页，PageCount是总条目数，这是必选参数，其它参数都是可选  
                    $("#Pagination").pagination(result, {
                        callback: PageCallback,
                        prev_text: ' ',       //上一页按钮里text  
                        next_text: ' ',       //下一页按钮里text  
                        items_per_page: pageSize,  //显示条数  
                        num_display_entries: 6,    //连续分页主体部分分页条目数  
                        current_page: pageIndex,   //当前页索引  
                        num_edge_entries: 2        //两侧首尾分页条目数  
                    });

                }
            });
        }
    });
}

///////////////