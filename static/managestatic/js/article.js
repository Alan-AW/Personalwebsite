$('#myButton').on('click', function () {
    let $btn = $(this).button('loading')
    $btn.button('提交')
})

tinyMCE.init({
    selector: '#tinymec',  // textarea ID
    language_url: '/static/tinymce/js/tinymce/langs/zh_CN.js',
    language: 'zh_CN',  // 语言
    directionality: 'ltr',  // 光标从左到右，rtl表示从右到左
    browser_spellcheck: true,
    contextmenu: false,
    height: '700',
    width: '770',
    plugins: [
        'advlist autolink lists link image charmap print preview anchor',
        'searchreplace visualblocks code fullscreen',
        'insertdatetime media table contextmenu paste imagetools wordcount',
        'code blockformats'
    ],
    toolbar: 'insertfile undo redo | styleselect | bld italic | alignleft aligncenter',
});

// 删除功能
function delete_article(pk) {
    let sure = confirm('确定要删除这篇文章吗？');
    if (!sure) {
        return;
    }
    $.ajax({
        url: '',
        type: 'post',
        data: {
            'csrfmiddlewaretoken': $("[name='csrfmiddlewaretoken']").val(),
            'ajax_type': 'delete',
            'pk': pk
        },
        success: function (data) {
            var del_status = JSON.parse(data);
            if (del_status === 'success') {
                window.location.reload();
            }
        }
    })
}

// 编辑功能
function change_article(pk) {
    let sure = confirm('确定要重新编辑这篇文章吗？');
    if (!sure) {
        return;
    }
    $.ajax({
        url: '',
        type: 'post',
        data: {
            'csrfmiddlewaretoken': $("[name='csrfmiddlewaretoken']").val(),
            'ajax_type': 'change',
            'pk': pk
        },
        success: function (data) {
            var edit_status = JSON.parse(data);
            if (edit_status === 'success') {
                window.location.reload();
            }
        }
    })
}
