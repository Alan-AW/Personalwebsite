$(function () {
    //窗体改变大小事件
    $(window).resize(function () {
        //正文高度
        var body_height = $(document.body).outerHeight(true);

        //底部元素高度
        var bottom_height = $(".all-footer").outerHeight(true);

        //浏览器页面高度
        var window_height = $(window).height();

        //判断并调整底部元素的样式
        if ($(".all-footer").hasClass('page-bottom')) {
            //若包含有page-bottom类，就应用了position设置
            //当position为absolute时，body高度不包含这个元素
            //所以页面高度需要判断body和footer之和若小于浏览器窗口
            //则移除样式，让footer自然跟随在正文后面
            if (body_height + bottom_height >= window_height) {
                $(".all-footer").removeClass('page-bottom');
            }
        } else {
            //若没有page-bottom类，body高度包含footer
            //判断body高度小于浏览器时，则悬浮于底部
            if (body_height < window_height) {
                $(".all-footer").addClass('page-bottom');
            }
        }
    });

    //页面加载时，模拟触发一下resize事件
    $(window).trigger('resize');
});