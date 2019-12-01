(function() {

    $(window).on('load', function() {

        //preloader code start
        var preloader = $('.loader-overlay');
        if(preloader.length) {
            preloader.fadeOut(1000, function () {
                //$(this).remove();
            });
        }
        //preloader code end

    });

    $(document).ready(function() {

        //scrolling to the top code start
        $("#to-top").click(function(){
            $("html, body").animate({
                scrollTop:0
            },500);
            return false;
        });
        function appearScroller() {
            if($(window).scrollTop() > 50){
                $("#to-top").addClass("active");
            } else {
                $("#to-top").removeClass("active");
            }
        }
        appearScroller();
        $(window).scroll(function(){
            appearScroller();
        });
        //scrolling to the top code end

        var url = 'li[id="' + window.location.pathname.split("/")[1] + '"]';
        $("#navbar-main").find(url).addClass("active");
        // console.log(url);
        // console.log($("#navbar-main").find(url).addClass("active"));
     

    });

})();