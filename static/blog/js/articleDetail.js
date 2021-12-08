// 点赞只对登录和非登录做了检测，所以同一个IP登录、退出均可以点赞，
// 后期修改认证机制，以ID作为处理依据
function likes() {
    let UserId = $('#UserIsSignin').attr('userid');
    let articleId = $('#articleId').attr('articleid');
    let token = $("[name='csrfmiddlewaretoken']").val();
    $countObj = $('#great-count');
    if (UserId) {
        user = UserId;
        isLogin = true;
    } else {
        user = 'get_ip_addrs';
        isLogin = false;
    }
    $.ajax({
        url: '',
        type: 'post',
        data: {
            'csrfmiddlewaretoken': token,
            'user': user,
            'articleId': articleId,
            'isLogin': isLogin
        },
        success: function (data) {
            let ReturnObj = JSON.parse(data);
            if (ReturnObj.success) {
                addMessage('success', '妙啊!(～￣▽￣)～');
                changeTheCommentNameColor();
                let count = parseInt($countObj.text());
                $countObj.text(count + 1);
            } else if (ReturnObj.serverOver) {
                addMessage('fail', '┗|｀O′|┛ 嗷~~ 真糟糕!服务器崩啦!');
            } else {
                addMessage('fail', '赞过了啦!(～￣▽￣)～');
            }
        }
    })
}

// 美化代码块
function beautiful() {
    if (!$('pre').hasClass('line-numbers')) {
        $('pre').addClass('line-numbers').before($(
            '<figcaption class="line-numbers-head">' +
            '<div class="custom-carbon">' +
            '<div class="custom-carbon-dot custom-carbon-dot--red"></div>' +
            '<div class="custom-carbon-dot custom-carbon-dot--yellow"></div>' +
            '<div class="custom-carbon-dot custom-carbon-dot--green"></div>' +
            '</div>' +
            '</figcaption>'
        ));
    }
}

beautiful()

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
// document.write(" 版本：");
// document.write(BomInfo.ver);

function randomColor() {
    let colorValue = ["#09ebfc", "#ff6651", "#ffb351", "#51ff65",
        "#5197ff", "#a551ff", "#ff51f7", "#ff518e",
        "#ff5163", "#efff51"];
    let x = 0;
    let y = 10;
    let Value = parseInt(Math.random() * (x - y + 1) + y);
    return colorValue[Value];
}

function changeTheCommentNameColor() {
    let rootNameObj = $('body').find('.root-comment-name');
    rootNameObj.css('color', randomColor());
    let replayNameObj = $('body').find('.replay-name');
    replayNameObj.css('color', randomColor());
}
changeTheCommentNameColor();

