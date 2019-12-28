$(function () {

    $('#button,#Retrievenow,#denglou').css('opacity', 0.7).hover(function () {
        $(this).stop().fadeTo(650, 1);
    }, function () {
        $(this).stop().fadeTo(650, 0.7);
    });
    if ($.cookie("codeusername") != null) {
        $.ajax({
            type: "POST",
            url: '/users/AjaxServer/checkis.ashx',
            data: { typex: 1 },
            async: false,
            success: function (data) {///去更新cookies
                if (data == "NotLogin") {
                    ///沒有登錄
                    getLogStatx(2); //没有记录cookies 的登录状态

                } else {
                    window.location.href = "http://home.wopop.com/UserHome/ot5lst/website.aspx";
                }
            }
        });


    }
    $("#button").click(function () {
        var username = $("#username").val();
        var userpwd = $("#userpwd").val();
        if (username.length > 0 && userpwd.length > 0) {
            getLogStatx(1);
        }

    });

    ////忘记密码
    $("#iforget").click(function () {
        $("#login_model").hide();
        $("#forget_model").show();

    });

    ///取回密码 
    $("#Retrievenow").click(function () {
        var usrmail = $("#usrmail").val();
        if (!Test_email(usrmail)) {
           // alert(msgggg.pssjs1);
            return false;
        }
        $.ajax({
            type: "POST",
            url: '/users/AjaxServer/checkis.ashx',
            data: { typex: 5, usrmail: usrmail },
            success: function (data) {//

                alert(data);
                $("#login_model").show();
                $("#forget_model").hide();
                $("#usrmail").val("");
                $("#username").val("");
                $("#userpwd").val("");

            }
        });


    });
    //返回
    $("#denglou").click(function () {
        $("#usrmail").val("");
        $("#username").val("");
        $("#userpwd").val("");
        $("#login_model").show();
        $("#forget_model").hide();

    });


    //typexx 自动 还是手动
    function getLogStatx(typex) {
        var current = (location.href);
        var screenwidth = $(window).width();
        var screenheight = $(window).height();
        var username = $("#username").val();
        var userpwd = $("#userpwd").val();
        var issavecookies = "NO";
        if ($("#save_me").attr("checked") == true) {
            issavecookies = "Yes";
        }
        else {
            issavecookies = "NO";
        }
        var l_dot = screenwidth + "*" + screenheight;
        if (typex == "2") {
            if (username == null && userpwd == null) {
                ////保存了cook
                username = $.cookie('codeusername');
                userpwd = $.cookie('codeppsd');
                $.ajax({
                    type: "POST",
                    url: '/users/AjaxServer/Ajax_User_Loading.ashx',
                    data: { username: username, userpwd: userpwd, issavecookies: issavecookies, l_dot: l_dot, typex: 2 },
                    success: function (data) {///去更新cookies
                        if (current.indexOf("index.aspx") > -1) {


                        } else {

                            if (data == "0" || data == "1") {
                                window.location.href = "http://home.wopop.com/UserHome/ot5lst/website.aspx";

                            } else {
                                ot5alert(data, "1");

                            }
                        }
                    }
                });


            }
        } else if (typex == "1") {
            ///// 手動 登錄
            $.ajax({
                type: "POST",
                url: '/users/AjaxServer/Ajax_User_Loading.ashx',
                data: { username: username, userpwd: userpwd, issavecookies: issavecookies, l_dot: l_dot, typex: 1 },
                success: function (data) {///去更新cookies
                    if (data == "0" || data == "1") {
                        window.location.href = "http://home.wopop.com/UserHome/ot5lst/website.aspx";

                    } else {
                        ot5alert(data, "1");

                    }
                }
            });
        }
    }


});
//Email 规则以后重新整理所有网站关于js 验证
function Test_email(strEmail) { var myReg = /^[-a-z0-9\._]+@([-a-z0-9\-]+\.)+[a-z0-9]{2,3}$/i; if (myReg.test(strEmail)) return true; return false; }
