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
tinyMCE.activeEditor.getBody().style.backgroundColor = '#000';