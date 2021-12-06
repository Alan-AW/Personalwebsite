function my_love() {
    $('.mask').on('click', click_mask);
    login_model();
}

//点击登录按钮弹出登录框
function login_model() {
    get_focus();
    $('.tyc-login').css({
        top: '50%',
        transform: 'translateY(-50%)',
        transition: 'all .6s ease',
        opacity: '.8'
    })
    $('.mask').css({
        display: 'block'
    })
}

// 点击遮罩层关闭弹出层
function click_mask() {
    $('.tyc-login').css({
        top: '-200px',
        transition: 'all .6s ease',
        opacity: '0'
    })
    $('.mask').css({
        display: 'none'
    })
}

// focus
function get_focus() {
    $('#username').focus();
}


function submit_eternal() {
    let name = $('#tyc-name').val();
    if (!name) {
        alert('必须要输入内容哦!');
        return;
    }
    $.ajax({
        url: '/tyc/',
        type: 'post',
        data: {
            'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
            'name': name
        },
        success: function (data) {
            let response = JSON.parse(data);
            click_mask();
            if (response.is_her) {
                location.href = '/tyc/';
            } else {
                alert('你不是我要等的人!');
            }
        }
    })
}

// //原生js实现login弹出框
// window.onload = function() {
//     function LoginModel(option) {
//         this.logintarget = option.logintarget;
//         this.masktarget = option.masktarget;
//     }
//     LoginModel.prototype.popLogin = function() {
//         this.logintarget.style.top = `50%`
//         this.logintarget.style.transform = 'translateY(-50%)'
//         this.logintarget.style.transition = 'all .6s ease'
//         this.logintarget.style.opacity = '1'
//         this.masktarget.style.display = 'block'
//     }
//     LoginModel.prototype.closePop = function() {
//         this.logintarget.style.top = `-400px`
//         this.logintarget.style.transition = 'all .6s ease'
//         this.logintarget.style.opacity = '0'
//         this.masktarget.style.display = 'none'
//     }

//     function getfocus() {
//         $('#username').focus()
//     }

//     //调用
//     var btn = document.querySelector('#btnlogin')
//     var login = document.querySelector('.login')
//     var mask = document.querySelector('.mask')
//     var LM = new LoginModel({
//         logintarget: login,
//         masktarget: mask
//     });
//     btn.addEventListener('click', function() {
//         LM.popLogin()
//         getfocus()
//     })
//     mask.addEventListener('click', function() {
//         LM.closePop()
//     })
// }
