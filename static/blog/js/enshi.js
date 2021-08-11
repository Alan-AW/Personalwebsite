// navgationback-color
$(function() {
	$(window).scroll(function() {
		if ($(window).scrollTop() > 300) {
			$('.nav').css({
				"background-color": "rgb(252,157,154)",
				"position": "fixed",
				"top": "0",
			});
			$('.nav-ul-li a').css("color", "whitesmoke");
		} else {
			$('.nav').css({
				"background-color": "rgba(240,240,240,.7)",
				"position": "",
			});
			$('.nav-ul-li a').css("color", "#999");
		}
	});
})
// fixed——left-nav
$(document).ready(function() {
	var scroh = $(".left-nav").offset().top;
	$(window).scroll(function() {
		if (scroh < $(window).scrollTop()) {
			var left = $(".left-nav").offset().left;
			$(".left-nav").css({
				'position': "fixed",
				'width': $(document.body).width() * 0.14,
				'top': '60',
			});
		} else {
			$(".left-nav").css({
				'position': "relative",
				'top': '0'
			});
		}
	});
});
// 锚点
function show_top(data) {
	var show_body = data + '-enshi';
	$('html,body').animate({
		scrollTop: $('.' + show_body).offset().top - 100
	}, 500);
}
