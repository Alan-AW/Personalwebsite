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

