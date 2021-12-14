from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponse, reverse
from django.views import View
from urllib.request import urlopen  # 向QQ发送请求
from urllib.parse import urlencode, parse_qs
from django.conf import settings as sys
from App_Users.models import OAuthRelationShip
import json, random, string
from random import shuffle


def qq_login(request):
    """
        使用QQ登录网站
    """
    code = request.GET.get('code')
    state = request.GET.get('state')
    if state != sys.QQ_STATE:
        raise Exception('state is error')
    # 获取access_token
    params = {
        'grant_type': 'authorization_code',
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
    openid = json.loads(data[10:-4]).get('openid')  # 唯一识别ID
    # 判断openid是否有关联的用户,有 --> 登陆；没有 --> 绑定一个用户
    oauth_obj = OAuthRelationShip.objects
    if oauth_obj.filter(open_id=openid, oauth_type=1).exists():
        realtion_ship = oauth_obj.get(open_id=openid, oauth_type=1)
        auth.login(request, realtion_ship)  # 登陆
        return redirect(reverse('blog:home'))
    else:
        bind_qq = Bind_QQ()
        bind_qq.bind_user(request, openid)
        return redirect(reverse('blog:home'))


class Bind_QQ(object):
    # 绑定用户QQ登陆信息
    def get_random_str(self, length):
        chars = string.ascii_letters + string.digits
        return ''.join([random.choice(chars) for i in range(length)])

    def get_username(self):
        # 为新用户创建8位随机用户名
        return self.get_random_str(8)

    def get_password(self):
        # 为新用户创建10位随机密码
        return self.get_random_str(10)

    def bind_user(self, request, openid):
        openid = request.session.pop('openid')  # 获取到这个ID之后便删除掉
        user = User.objects.create_user(username=self.get_username(), password=self.get_password())
        # 记录关系
        relationship = OAuthRelationShip()
        relationship.user = user
        relationship.open_id = openid
        relationship.oaurh_type = 1
        relationship.save()
        # 用户登陆
        auth.login(request, user)



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
