// 导航点击选中效果
$('.li').click(function () {
    for (let i = 0; i < $('.li').length + 1; i++) {
        $('li').eq(i).attr('class', 'li');
    }
    $(this).attr('class', 'active');
});
