$('#myButton').on('click', function () {
	let $btn = $(this).button('loading')
	$btn.button('提交')
})

// 编辑和删除功能
function change_article(make, pk) {
	let sure = confirm('你确定要' + '"' + make + '"' + '这篇文章吗?');
	if (!sure) {
		return;
	}
	$.ajax({
		url: '',
		type: 'post',
		data: {
			csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
			ajax_type: make,
			pk: pk
		},
		success: function (response) {
			let make_status = JSON.parse(response);
			if (make_status === 'success') {
				window.location.reload();
			} else if (make_status.edit_msg === 'True') {
				$('.form_action').attr('action', '?type=update')
				$('#article_title').val(make_status.title);
				$('#tinymec').val(make_status.body);
				$('#tags').val(make_status.tags);
				$('#category').val(make_status.category);
			}
		}
	})
}
