$(document).ready(function () {
	$(".animsition").animsition({
		inClass: 'fade-in-down', // 进入页面时的动画属性
		outClass: 'fade-out-top', // 离开页面时的动画属性
		inDuration: 1500,
		outDuration: 800,
		linkElement: '.animsition-link',
		// e.g. linkElement: 'a:not([target="_blank"]):not([href^="#"])'
		loading: true,
		loadingParentElement: 'body', //animsition wrapper element
		loadingClass: 'animsition-loading',
		loadingInner: '', // e.g '<img src="loading.svg" />'
		timeout: false,
		timeoutCountdown: 5000,
		onLoadEvent: true,
		browser: ['animation-duration', '-webkit-animation-duration'],
		// "browser" option allows you to disable the "animsition" in case the css property in the array is not supported by your browser.
		// The default setting is to disable the "animsition" in a browser that does not support "animation-duration".
		overlay: false,
		overlayClass: 'animsition-overlay-slide',
		overlayParentElement: 'body',
		transition: function (url) {
			window.location.href = url;
		}
	});
});

// 修改用户名
function change_uname() {
	$('.username_input').focus(function () {
		$('.edit_username').removeClass('hidden');
	});

	$('.username_input').blur(function () {
		// $('.edit_username').addClass('hidden');
	});

	$('.username_input').on('input', function () {
		// alert('正在修改昵称');
	})
}

change_uname();


function edit_username(pk) {
	$.ajax({
		url: '',
		type: 'post',
		data: {
			'csrfmiddlewaretoken': $("[name='csrfmiddlewaretoken']").val(),
			'pk': pk,
			'name': $('.username_input').val(),
		},
		success: function (data) {
			let response = JSON.parse(data);
			if (response.statue) {
				alert('修改成功!');
				$('.edit_username').addClass('hidden');
				$('.username_input').val(response.new_name);
			} else {
				alert(response.error_msg);
			}
		}
	})
}