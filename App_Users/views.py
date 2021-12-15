from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponse, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from urllib.request import urlopen  # 向QQ发送请求
from urllib.parse import urlencode, parse_qs
from django.conf import settings as sys
from App_Users.models import OAuthRelationShip
import json, random, string
from random import shuffle


class BindQQ(object):
    # 绑定用户QQ登陆信息
    def __init__(self, request, params, openid):
        self.request = request
        self.nickname = params.get('qq_nickname')
        self.avatar = params.get('qq_avatar')
        self.openid = openid

    def get_random_str(self, length):
        # 生成指定随机字符串
        chars = string.ascii_letters + string.digits
        return ''.join([random.choice(chars) for i in range(length)])

    def get_username(self):
        # 为新用户创建8位随机用户名
        return self.nickname + self.get_random_str(4)

    def get_password(self):
        # 为新用户创建10位随机密码
        return self.get_random_str(12)

    def bind_user(self):
        # openid = request.session.pop('openid')  # 获取到这个ID之后便删除掉
        user = User.objects.create_user(username=self.get_username(), password=self.get_password())
        # 记录关系
        relationship = OAuthRelationShip()
        relationship.open_id = self.openid
        relationship.oauth_type = 1
        relationship.nickname = self.nickname
        relationship.avatar = self.avatar
        relationship.save()
        # 用户登陆
        auth.login(self.request, user)


def get_qq_user_msg(access_token, openid):
    # 获取用户QQ信息
    params = {
        'access_token': access_token,
        'oauth_consumer_key': sys.QQ_APP_ID,
        'openid': openid,
    }
    response = urlopen('https://graph.qq.com/user/get_user_info?' + urlencode(params))
    data = json.loads(response.read().decode('utf8'))
    params = {
        'qq_nickname': data.get('nickname'),  # QQ用户昵称
        'qq_avatar': data.get('figureurl_qq_1')  # 40*40头像
    }
    return params


class QQLogin(View):
    def get(self, request):
        """
        使用QQ登录网站对回调域地址的处理
        """
        code = request.GET.get('code')
        state = request.GET.get('state')
        if state != sys.QQ_STATE:
            return HttpResponse('State Code Error')
        # 1.获取access_token
        params = {
            'grant_type': 'authorization_code',
            'client_id': sys.QQ_APP_ID,
            'client_secret': sys.QQ_APP_KEY,
            'code': code,
            'redirect_uri': sys.QQ_REDIRECT_URL
        }
        url = 'https://graph.qq.com/oauth2.0/token?%s' % urlencode(params)
        response = urlopen(url)
        data = parse_qs(response.read().decode('utf8'))
        access_token = data.get('access_token')[0]

        # 2.获取openid
        response = urlopen('https://graph.qq.com/oauth2.0/me?access_token=%s' % access_token)
        data = response.read().decode('utf8')
        openid = json.loads(data[10:-4]).get('openid')  # 唯一识别ID

        # 3.判断openid是否有关联的用户,有 --> 登陆；没有 --> 绑定一个用户
        oauth_obj = OAuthRelationShip.objects
        if oauth_obj.filter(open_id=openid, oauth_type=1).exists():
            relation_ship = oauth_obj.get(open_id=openid, oauth_type=1)
            params = get_qq_user_msg(access_token, openid)
            auth.login(request, relation_ship.user)  # 登陆
            return redirect(reverse('blog:home') + '?' + urlencode(params))
        else:
            # 获取QQ用户信息（昵称和头像）
            params = get_qq_user_msg(access_token, openid)
            # 绑定QQ用户
            bind_qq = BindQQ(request, params, openid)
            bind_qq.bind_user()
            return redirect(reverse('blog:home') + '?' + urlencode(params))


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


class UserDetail(LoginRequiredMixin, View):
    # 用户详情页
    def get(self, request):
        user_obj = request.user
        username = user_obj.username
        date_joined = user_obj.date_joined
        is_qq_user = OAuthRelationShip.objects.filter(user=user_obj).exists()
        is_super = user_obj.is_superuser
        if is_qq_user:
            qq_user_obj = OAuthRelationShip.objects.filter(user=user_obj).first()
            qq_nick_name = qq_user_obj.nickname
            qq_avatar = qq_user_obj.avata
        return render(request, 'users/user_detail.html', locals())
