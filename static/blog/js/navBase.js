let mouseMoved = 0; //从鼠标进入banner起向右移动的距离与屏幕宽度的比
let mouseIn; //鼠标进入banner时，鼠标左边部分宽度与屏幕宽度的比

const header = document.querySelector('header');
const canvas = document.querySelector('#snow-foreground');
//各层图片
const day = document.querySelector('#day');
const sunset = document.querySelector('#sunset');
const snowball = document.querySelector('#snowball');
const night = document.querySelector('#night');
const fog = document.querySelector('#fog');
const treeDay = document.querySelector('#tree-day');
const treeSunset = document.querySelector('#tree-sunset');
const treeNight = document.querySelector('#tree-night');

header.addEventListener('mouseenter', ({clientX}) => mouseIn = clientX / innerWidth);
header.addEventListener('mousemove', ({clientX}) => mouseMoved = clientX / innerWidth - mouseIn);
header.addEventListener('mouseleave', () => {
    //鼠标离开banner时，慢慢复原到日落状态
    let start = Date.now();
    let mouseMovedBeforeReset = mouseMoved;
    let restore = setInterval(() => {
        let progress = (Date.now() - start) / 250;
        mouseMoved = mouseMovedBeforeReset * (1 - progress);
        if (progress >= 1) {
            mouseMoved = 0;
            clearInterval(restore);
        }
        computeStyles();
    }, 10);
});
const applyTransform = (translateX = 0, translateY = 0, rotate = 0, scale = 1) => `scale(${scale}) translate(${translateX}px, ${translateY}px) rotate(${rotate}deg)`;

function computeStyles() {
    //计算图片的位移、不透明度、旋转角度、缩放、模糊度。
    //document.querySelector('#debug').innerText = `鼠标进入：${mouseIn}  鼠标移动：${mouseMoved}`;

    //模糊度固定不变
    treeDay.style.filter = treeSunset.style.filter = 'blur(2px)';
    treeNight.style.filter = 'blur(5px)';

    //鼠标移动1个屏幕的宽度时，雪球转6deg，左移顺时针，右移逆时针，默认10deg
    const rotationOfSnowball = 10 - 6 * mouseMoved;

    //雪球、景和树的不透明度同步变化（虽然从B站上观测到不是这样，但作者懒得细究其变化关系）
    day.style.opacity = treeDay.style.opacity = 1;
    snowball.style.opacity = sunset.style.opacity = treeSunset.style.opacity = Math.min(Math.max(2.5 * mouseMoved + 1, 0), 1);
    night.style.opacity = treeNight.style.opacity = Math.max(mouseMoved * 2.5, 0);

    //在夜景不透明后，雾才开始不透明
    fog.style.opacity = Math.max(0, mouseMoved * 3.75 - 1.5);

    //景位移
    const rangeOfMovement = innerWidth * 0.025 + 36.345; //可移动范围
    const movementOfScene = mouseMoved * -rangeOfMovement;

    //树移动得快点儿
    const movementOfTrees = movementOfScene * 1.5;

    //雪球位移
    const translateYOfSnowball = -10 * mouseMoved ** 2 - 60 * mouseMoved + 20;
    const translateXOfSnowball = movementOfScene * -2;

    //应用各transform属性
    fog.style.transform = day.style.transform = sunset.style.transform = night.style.transform = applyTransform(movementOfScene);
    treeDay.style.transform = treeSunset.style.transform = treeNight.style.transform = applyTransform(movementOfTrees);
    snowball.style.transform = applyTransform(translateXOfSnowball, translateYOfSnowball, rotationOfSnowball);
}

computeStyles();
header.addEventListener('mousemove', computeStyles);
addEventListener('resize', () => {
    let {height, width} = getComputedStyle(header);
    canvas.height = parseFloat(height);
    canvas.width = parseFloat(width);
});
dispatchEvent(new Event('resize'));

// HTML区域点击生成上浮文字
$(function () {
    let a_idx = 0,
        b_idx = 0;
    c_idx = 0;
    jQuery(document).ready(function ($) {
        $("html").click(function (e) {
            let a = ["欢迎你", "么么哒", "你真好", "雅蠛蝶", "棒棒哒", "真可爱", "你最美", "喜欢你", "真聪明", "爱你哦",
                    "好厉害", "你真帅", "哈拉少"
                ],
                b = ["#09ebfc", "#ff6651", "#ffb351", "#51ff65",
                    "#5197ff", "#a551ff", "#ff51f7", "#ff518e",
                    "#ff5163", "#efff51"
                ],
                c = ["12", "14", "16", "18", "20"];
            let $i = $("<span/>").text(a[a_idx]);
            a_idx = (a_idx + 1) % a.length;
            b_idx = (b_idx + 1) % b.length;
            c_idx = (c_idx + 1) % c.length;
            let x = e.pageX,
                y = e.pageY;
            $i.css({
                "z-index": 999,
                "top": y - 20,
                "left": x,
                "position": "absolute",
                "font-weight": "bold",
                "font-size": c[c_idx] + "px",
                "color": b[b_idx]
            });
            $("body").append($i);
            $i.animate({
                "top": y - 180,
                "opacity": 0
            }, 1500, function () {
                $i.remove();
            });
        });
    });
    var _hmt = _hmt || [];
})

// back to top
$(function () {
    //先将#back-top隐藏
    $('#back-top').hide();
    //当滚动条的垂直位置距顶部100像素一下时，跳转链接出现，否则消失
    $(window).scroll(function () {
        if ($(window).scrollTop() > 100) {
            $('#back-top').fadeIn(1000);
            $("#navgation").css({
                "background-color": "rgb(252,157,154)",
            });
        } else {
            $("#back-top").fadeOut(1000);
            $("#navgation").css({
                "background-color": "rgba(0,0,0,0)"
            });
        }
    });
    //点击跳转链接，滚动条跳到0的位置，页面移动速度是1000
    $("#back-top").click(function () {
        $('html').animate({
            scrollTop: '0'
        }, 1000);
        return false; //防止默认事件行为
    })
})

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

// 和风天气网免费API
// https://widget.qweather.com/
WIDGET = {
    "CONFIG": {
        "layout": "2",
        "width": 230,
        "height": 270,
        "background": "5",
        "dataColor": "434343",
        "borderRadius": "12",
        "key": "6e657ca3f6db4f42b0629b6c733a9fec"
    }
}

// 一言API
function _random() {
    $.ajax({
        type: 'GET',
        url: 'https://v1.hitokoto.cn',
        dataType: 'jsonp',
        jsonp: 'callback',
        jsonpCallback: 'hitokoto',
        success(data) {
            let response = JSON.parse(data);
            // $('#hitokoto_text').attr('href', 'https://hitokoto.cn/?uuid=' + response.uuid);
            $('#hitokoto').addClass('hitokoto');
            $('#hitokoto').html(response.hitokoto);
        },
        error(jqXHR, textStatus, errorThrown) {
            // 错误信息处理
            console.error(textStatus, errorThrown)
        }
    })
}

setInterval('_random()', 6000); // 间隔6秒

// 仿预加载进度条---封装
class TopProgress {
    constructor() {
        if (!TopProgress.instance) {
            TopProgress.instance = this;
        }
        this.getDiv()
        this.width = 0
        this.state = 0 // start
        this.interID = null
        return TopProgress.instance
    }

    getDiv() {
        this.topProgress = document.querySelector('.top-progress')

        if (!this.topProgress) {
            this.topProgress = document.createElement('div')
            this.topProgress.className = 'top-progress'
            document.body.appendChild(this.topProgress)
            this.css('position', 'fixed')
            this.css('top', '0')
            this.css('height', '6px')
            this.css('width', '100%')
            this.css('backgroundColor', 'rgb(37, 206, 195)')
            this.css('transform', 'translate3d(-100%, 0px, 0px)')
            this.css('transition', 'all 0.01s')
        }
    }

    css(key, value) {
        this.topProgress.style[key] = value
    }

    static 'set'(pre) {
        let tp = new TopProgress()
        tp.width = pre * 100
        tp.css('transition', 'all 0.1s')
        tp.css('transform', `translate3d(-${100 - this.width}%, 0px, 0px)`)
    }

    static start() {
        let tp = new TopProgress()
        let topProgress = tp.topProgress

        tp.interID = setInterval(() => {
            topProgress.offsetWidth
            topProgress.style.transition = 'all 0.01s'
            topProgress.style.transform = `translate3d(-${100 - tp.width}%, 0,0)`
            if (tp.state != 1 && tp.width < 90) {
                tp.width += 0.4
            }
        }, 10)
    }

    static complete() {
        let tp = new TopProgress()
        let topProgress = tp.topProgress
        tp.state = 1
        tp.css('transition', 'all 0.1s')
        tp.css('transform', 'translate3d(0, 0,0)')
        clearInterval(tp.interID)
        setTimeout(() => {
            tp.css('backgroundColor', 'rgba(0, 0, 0, 0)')
        }, 300)
    }
}

TopProgress.start()
new Promise((resolve, reject) => {
    setTimeout(() => {
        resolve(1)
    }, 2000)
}).then((res) => {
    TopProgress.complete()
})

// 固定左右两侧在顶部
$(document).ready(function () {
    let scroh = $(".all-left").offset().top;
    $(window).scroll(function () {
        if (scroh < $(window).scrollTop()) {
            //获取div距离
            let left = $(".all-left").offset().left;
            $(".all-left").css({
                'position': "fixed",
                'left': 'left' - $(".all-left").css('width'),
                'top': '150',
                'margin-top': '0'
            });
        } else {
            $(".all-left").css({
                'position': "relative",
            });
        }
    });
});

$(document).ready(function () {
    let scroh = $(".all-right").offset().top;
    $(window).scroll(function () {
        if (scroh < $(window).scrollTop()) {
            //获取div距离
            let right = $(".all-right").offset().right;
            $(".all-right").css({
                'position': "fixed",
                'float': 'right',
                'right': '0',
                'top': '150',
                'margin-top': '0'
            });
        } else {
            $(".all-right").css({
                'position': "relative",
            });
        }
    });
});