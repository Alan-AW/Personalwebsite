// 定位
var map = new BMap.Map("allmap");
var point = new BMap.Point(116.331398, 39.897445);
map.centerAndZoom(point, 12);

function myFun(result) {
    var cityName = result.name;
    map.setCenter(cityName);
    $('#baidumap').val(cityName);
}

var myCity = new BMap.LocalCity();
myCity.get(myFun);

// 获取用户浏览器类型
function getBrowserInfo() {
    var Info = {};
    var str = window.navigator.userAgent.toLowerCase();
    var bReg = /(msie|firefox|chrome|opera|version).*?([\d.]+)/;
    var infoArr = str.match(bReg);
    Info.browser = infoArr[1].replace(/version/, "safari");
    Info.ver = infoArr[2];
    return Info;
}

var BomInfo = getBrowserInfo();
var userBrowser = BomInfo.browser;
var userBrowserVer = BomInfo.ver;


