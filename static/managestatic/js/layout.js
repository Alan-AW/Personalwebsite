// 导航点击改变背景颜色
$('.li').click(function () {
    for (var i = 0; i < $('.li').length + 1; i++) {
        $('li').eq(i).attr('class', 'li');
    }
    $(this).attr('class', 'active');
});
