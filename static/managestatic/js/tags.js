function edit_tags(pk) {
    let is_hidden = $('.tags_row').hasClass('hidden');
    if (is_hidden) {
        $('.tags_row').removeClass('hidden');
    } else {
        $('.tags_row').addClass('hidden');
    }
    $('#edit_tags_id').val(pk);
}

function submit_tags() {
    let tags_pk = $('#edit_tags_id').val();
    let tags_title = $('#edit_tags_input').val();
    if (!tags_pk || !tags_title) {
        return alert('参数不全!无法提交');
    }
    $.ajax({
        url: '',
        type: 'post',
        data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            post_type: 'edit_tags',
            pk: tags_pk,
            title: tags_title,
        },
        success: function (data) {
            let response = JSON.parse(data);
            if (response === 'success') {
                $('#edit_tags_id').val('');
                $('.tags_row').addClass('hidden');
                window.location.reload();
            } else {
                alert('操作失败!');
                window.location.reload();
            }

        }
    })
}