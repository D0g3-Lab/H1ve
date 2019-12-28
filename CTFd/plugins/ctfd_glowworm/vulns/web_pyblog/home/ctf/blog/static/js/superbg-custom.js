jQuery(function($){

    $.supersized({

        // Functionality
        slide_interval     : 20000,    // 切换时间
        transition         : 1,    // 0-None, 1-Fade, 2-Slide Top, 3-Slide Right, 4-Slide Bottom, 5-Slide Left, 6-Carousel Right, 7-Carousel Left
        transition_speed   : 3000,    // 过度时间
        performance        : 1,    // 0-Normal, 1-混合速度/质量, 2-优化图像质量, 3-优化转换速度 // (仅适用于Firefox或IE，不是WebKit)

        // Size & Position
        min_width          : 0,    // 允许的最小宽度 (in pixels)
        min_height         : 0,    // 允许的最小高度 (in pixels)
        vertical_center    : 1,    // 垂直中心背景
        horizontal_center  : 1,    // 水平中心背景
        fit_always         : 0,    // 图像永远不会超过浏览器的宽度或高度 (Ignores min. dimensions)
        fit_portrait       : 1,    // 肖像图片将不超过浏览器高度
        fit_landscape      : 0,    // 景观图像不超过浏览器宽度

        // Components
        slide_links        : 'blank',    // Individual links for each slide (Options: false, 'num', 'name', 'blank')
        slides             : [    // Slideshow Images
								 {image : '/static/images/bgimg/bg0.jpg'},
                                 {image : '/static/images/bgimg/bg1.jpg'},
                                 {image : '/static/images/bgimg/bg2.jpg'},
                                 {image : '/static/images/bgimg/bg3.jpg'},
								 {image : '/static/images/bgimg/bg4.jpg'}
                             ]

    });

});
