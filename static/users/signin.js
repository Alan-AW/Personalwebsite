// 获取元素和点击操作
const signInBtn = document.getElementById("signIn");
const signUpBtn = document.getElementById("signUp");
const fistForm = document.getElementById("form1");
const secondForm = document.getElementById("form2");
const container = document.querySelector(".container");

signInBtn.addEventListener("click", () => {
    container.classList.remove("right-panel-active");
});

signUpBtn.addEventListener("click", () => {
    container.classList.add("right-panel-active");
});

fistForm.addEventListener("submit", (e) => e.preventDefault());
secondForm.addEventListener("submit", (e) => e.preventDefault());


// 登录按钮
$('#submitBtn-signin').click(function () {
    var username = $('#signin-user-name').val();
    var pwd = $('#signin-user-pwd').val();
    var token = $("[name='csrfmiddlewaretoken']").val();
    if (!username) {
        alert('请输入用户名!');
    } else if (!pwd) {
        alert('请输入密码!');
    } else {
        $.ajax({
            url: '',
            type: 'post',
            data: {
                'username': username,
                'pwd': pwd,
                'make': 'signin',
                'csrfmiddlewaretoken': token
            },
            success: function (data) {
                var returnObj = JSON.parse(data);
                if (returnObj.error) {
                    alert('邮箱格式错误!');
                } else if (returnObj.not_has_user) {
                    var to_register = confirm('该用户名不存在，您希望用此用户名进行注册吗？');
                    if (to_register) {
                        window.location.reload();  // 刷新页面
                    } else {
                        $('#signin-user-name').val('');
                        $('#signin-user-pwd').val('');
                    }
                } else if (returnObj.UserIsSignin) {
                    alert('您已经登录了!请不要重复登录!');
                } else if (returnObj.is_signin) {
                    location.href = '/blog/home/';
                } else {
                    alert('(￣_￣|||) 登录失败!请检查后重试!');
                    $('#signin-user-name').val('');
                    $('#signin-user-pwd').val('');
                }
            }
        })
    }
})

// 注册按钮
$('#submitBtn-register').click(function () {
    var username = $('#register-user-name').val();
    var pwd = $('#register-user-pwd').val();
    const token = $("[name='csrfmiddlewaretoken']").val();
    if (!username) {
        alert('请输入用户名!');
    } else if (!pwd) {
        alert('请输入密码!');
    } else if (pwd.length < 8) {
        alert('密码长度不能小于8位!');
    } else {
        var sure = confirm('您确定使用:  ' + username + '  进行注册嘛？');
        if (sure) {
            $.ajax({
                url: '',
                type: 'post',
                data: {
                    'username': username,
                    'pwd': pwd,
                    'make': 'register',
                    'csrfmiddlewaretoken': token
                },
                success: function (data) {
                    var returnObj = JSON.parse(data);
                    if (returnObj.error) {
                        alert('格式错误!');
                    } else if (returnObj.is_register) {
                        alert('恭喜您注册成功!');
                        location.href = '';
                    } else if (returnObj.hasUser) {
                        var forgetPwd = confirm('改用户名已经被注册了哦,忘记了密码嘛？');
                        if (forgetPwd) {
                            forgot();
                            $('#register-user-name').val('');
                            $('#register-user-pwd').val('');
                        } else {
                            $('#register-user-name').val('');
                            $('#register-user-pwd').val('');
                        }
                    } else {
                        alert('(￣_￣|||) 注册失败了,请检查后重试!!');
                        $('#register-user-name').val('');
                        $('#register-user-pwd').val('');
                    }
                }
            })
        }
    }
})


function forgot() {
    $('.theme-popover-mask').fadeIn(100);
    $('.theme-popover').slideDown(200);
}

function close() {
    $('.theme-popover-mask').fadeOut(100);
    $('.theme-popover').slideUp(200);
}

function submitNewPwd() {
    var username = $('#forgotName').val();
    var pwd = $('#forgotPwd').val();
    var token = $("[name='csrfmiddlewaretoken']").val();
    if (!username || !pwd) {
        alert('请输入完整信息!');
        return false;
    }
    $.ajax({
        url: '/users/forgotPwd/',
        type: 'post',
        data: {
            'username': username,
            'pwd': pwd,
            'csrfmiddlewaretoken': token
        },
        success: function (data) {
            var status = JSON.parse(data);
            if (status.isSupperUser) {
                alert('您没有权限修改超级用户的密码!');
                close();
                return false;
            }
            if (status.success) {
                alert('密码修改成功!');
                close();
            } else {
                alert('密码修改失败!请检查后重试...');
            }
        }
    })
}