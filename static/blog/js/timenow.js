// 时间戳
let strtime = '2021-12-1';

//当前时间时间戳
function foxc() {
    let nowTime = (Date.parse(new Date())) / 1000;
    // let date = new Date(strtime); //传入一个时间格式，如果不传入就是获取现在的时间了，这样做不兼容火狐。
    // 兼容火狐
    let date = new Date(strtime.replace(/-/g, '/'));
    let time3 = (Date.parse(date)) / 1000;
    let time4 = nowTime - time3;
    let timeDay = Math.floor(time4 / 60 / 60 / 24);
    let timeHour = Math.floor(time4 / 60 / 60) - timeDay * 24;
    let timeMinute = Math.floor(time4 / 60) - timeDay * 24 * 60 - timeHour * 60;
    let timeSecond = Math.floor(time4) - timeDay * 24 * 60 * 60 - timeHour * 60 * 60 - timeMinute * 60;
    document.getElementById("timeDay").innerHTML = timeDay;
    document.getElementById("timeHour").innerHTML = timeHour;
    document.getElementById("timeMinute").innerHTML = timeMinute;
    document.getElementById("timeSecond").innerHTML = timeSecond;
}

window.setInterval(foxc, 1000)
