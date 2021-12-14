from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.views import View
from urllib.request import urlopen  # 向QQ发送请求
from urllib.parse import urlencode, parse_qs
from django.conf import settings as sys
import json
from random import shuffle


class QQLoginIn(View):
    """
    使用QQ登录网站
    """

    def get(self, request):
        code = request.GET.get('code')
        state = request.GET.get('state')
        if state != sys.QQ_STATE:
            raise Exception('state is error')
        # 获取access_token
        params = {
            'grant_type': '',
            'client_id': sys.QQ_APP_ID,
            'client_secret': sys.QQ_APP_KEY,
            'code': code,
            'redirect_uri': sys.QQ_REDIRECT_URL
        }
        url = 'https://graph.qq.com/oauth2.0/authorize?' + urlencode(params)
        response = urlopen(url)
        data = parse_qs(response.read().decode('utf8'))
        access_token = data.get('access_token')[0]
        # 获取openid
        response = urlopen('https://graph.qq.com/oauth2.0/me?access_token=%s' % access_token)
        data = response.read().decode('utf8')
        openid = json.loads(data[10:-4]).get('openid')



"""
grant_type	必须	授权类型，在本步骤中，此值为“authorization_code”。
client_id	必须	申请QQ登录成功后，分配给网站的appid。
client_secret	必须	申请QQ登录成功后，分配给网站的appkey。
code	必须	上一步返回的authorization code。
如果用户成功登录并授权，则会跳转到指定的回调地址，并在URL中带上Authorization Code。
例如，回调地址为www.qq.com/my.php，则跳转到：
http://www.qq.com/my.php?code=520DD95263C1CFEA087******
注意此code会在10分钟内过期。
redirect_uri	必须	与上面一步中传入的redirect_uri保持一致。
"""


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
