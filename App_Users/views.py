import json
from random import shuffle
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.views import View


class Signin(View):
    """
    登录、注册
    """

    def get(self, request):
        return render(request, 'users/signinview.html')

    def shuffle_str(self, s):
        str_list = list(s)
        shuffle(str_list)
        return ''.join(str_list)

    def post(self, request):
        if request.is_ajax():
            make = request.POST['make']
            username = request.POST['username']
            pwd = request.POST['pwd']
            Result = {}
            hasUser = User.objects.filter(username=username)
            if make == 'signin':
                if not hasUser:
                    Result['not_has_user'] = True
                    return HttpResponse(json.dumps(Result))
                # 禁止已登录用户再次登录！！！！
                # 应该从session来判断--而不是修改 is_active字段 = False
                if hasUser:
                    authUser = auth.authenticate(username=username, password=pwd)
                    if authUser:
                        auth.login(request, authUser)
                        Result['is_signin'] = True
                    else:
                        Result['is_signin'] = False
                else:
                    Result['not_has_user'] = True
            elif make == 'register':
                Result = {'is_register': False}
                if not hasUser:
                    User.objects.create_user(username=username, password=pwd)
                    Result['is_register'] = True
                else:
                    Result['hasUser'] = True
            return HttpResponse(json.dumps(Result))
        else:
            cnm = '本次提交存在违法操作！您已被系统标记'
            return HttpResponse(json.dumps(cnm))


class Logout(View):
    """
    退出登录
    """

    def get(self, request):
        auth.logout(request)
        url = reverse('blog:home')
        return redirect(url)


class ForgotPwd(View):
    """
    忘记密码
    """
    def post(self, request):
        if request.is_ajax():
            status = {}
            username = request.POST['username']
            pwd = request.POST['pwd']
            if username == 'xmj':
                status['isSupperUser'] = True
                return HttpResponse(json.dumps(status))
            if all([username, pwd]):
                userObj = User.objects.filter(username=username).first()
                if userObj:
                    try:
                        userObj.set_password(pwd)
                        userObj.save()
                        status['success'] = True
                    except:
                        status['success'] = False
                else:
                    status['success'] = False
            else:
                status['success'] = False
            return HttpResponse(json.dumps(status))
        else:
            cnm = '本次提交存在违法操作！您已被系统标记'
            return HttpResponse(json.dumps(cnm))


class UseQQToLoginIn(View):
    """
    使用QQ登录网站
    """

    def get(self, request):
        pass
