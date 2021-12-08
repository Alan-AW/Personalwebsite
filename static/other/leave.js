// 获取用户浏览器类型
function getBrowserInfo() {
	let Info = {};
	let str = window.navigator.userAgent.toLowerCase();
	let bReg = /(msie|firefox|chrome|opera|version).*?([\d.]+)/;
	let infoArr = str.match(bReg);
	Info.browser = infoArr[1].replace(/version/, "safari");
	Info.ver = infoArr[2];
	return Info;
}

let BomInfo = getBrowserInfo();
let userBrowser = BomInfo.browser;
let userBrowserVer = BomInfo.ver;

