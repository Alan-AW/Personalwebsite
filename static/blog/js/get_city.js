$(function() {
	//获取城市ajax
	// let url = 'https://api.map.baidu.com/location/ip?ak=eGoFmU42VgXFh2OjzSjcPgd5PunNWu6p&s=1';  // 上线
	let url = 'http://api.map.baidu.com/location/ip?ak=eGoFmU42VgXFh2OjzSjcPgd5PunNWu6p';  // 开发
	$.ajax({
		url: url,
		type: 'POST',
		dataType: 'jsonp',
		success: function(data) {
			if (JSON.stringify(data.content.address_detail.city)) {
				$('#city').html(JSON.stringify(data.content.address_detail.city));
			} else {
				$('#city').html(JSON.stringify(data.content.address_detail.province));
			}
		}
	});
})
