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
from App_Users.tools.get_qq_msg import get_qq_user_msg
from App_Blog.models import LeaveMsg
from APP_Comment.models import Comment
import time, re


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
        relationship.user = user
        relationship.open_id = self.openid
        relationship.oauth_type = 1
        relationship.nickname = self.nickname
        relationship.avatar = self.avatar
        relationship.save()
        # 用户登陆
        auth.login(self.request, user)


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
            # 更新头像和昵称信息
            relation_ship.avatar = params.get('qq_avatar')
            relation_ship.nickname = params.get('qq_nickname')
            relation_ship.save()
            # 登陆
            auth.login(request, relation_ship.user)
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
        return redirect(reverse('blog:home'))


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
        user_detail_dict = {}
        username = user_obj.username
        email = user_obj.email
        date_joined = user_obj.date_joined
        is_qq_user = OAuthRelationShip.objects.filter(user=user_obj)
        is_super = user_obj.is_superuser
        if is_qq_user:
            qq_user_obj = OAuthRelationShip.objects.filter(user=user_obj).first()
            qq_nick_name = qq_user_obj.nickname
            qq_avatar = qq_user_obj.avatar
        else:
            qq_nick_name, qq_avatar = None, None
        comment_count = Comment.objects.filter(user=user_obj).count()
        leave_count = LeaveMsg.objects.filter(name=username).count()
        user_detail_dict = {
            'username': username,
            'email': email,
            'date_joined': date_joined,
            'is_qq_user': is_qq_user,
            'qq_nickname': qq_nick_name,
            'qq_avatar': qq_avatar,
            'date_count': self.get_date(user_obj),
            'comment_count': comment_count,
            'leave_count': leave_count
        }
        return render(request, 'users/user_detail.html', locals())

    def post(self, request):
        if request.is_ajax():
            response = {'statue': False}
            pk = request.POST.get('pk')
            name = request.POST.get('name')
            email = request.POST.get('email')
            try:
                user_obj = User.objects.get(id=pk)
            except Exception:
                user_obj = None
            if user_obj and user_obj.email == email:
                response['error_msg'] = '与原邮箱一致!'
                return HttpResponse(json.dumps(response))
            if user_obj and user_obj.username == name:
                response['error_msg'] = '与原用户名一致!'
                return HttpResponse(json.dumps(response))
            email_addrs = r'^[0-9a-zA-Z_]{1,19}@[0-9a-zA-Z]{1,13}\.[a-zA-Z]{2,3}$'
            check_email = re.match(email_addrs, email)
            if email and check_email:
                try:
                    user_obj.email = email
                    user_obj.save()
                    response['statue'] = True
                    response['new_email'] = email
                except Exception:
                    response['error_msg'] = '数据错误!请稍后再试!'
                return HttpResponse(json.dumps(response))
            if len(name) >= 1:
                try:
                    user_obj.username = name
                    user_obj.save()
                    response['statue'] = True
                    response['new_name'] = name
                except Exception:
                    response['error_msg'] = '用户不存在!'
            else:
                response['error_msg'] = '您的输入有误!请重新输入!'
            return HttpResponse(json.dumps(response))

    def get_date(self, user):
        use_join = str(user.date_joined.date())
        sys_time = time.gmtime()
        sys_y, sys_m, sys_d = sys_time.tm_year, sys_time.tm_mon, sys_time.tm_mday
        use_y, use_m, use_d = use_join.split('-')
        year = int(sys_y) - int(use_y)
        year = year * 365
        month = max(int(use_m), int(sys_m)) - min(int(use_m), int(sys_m))
        month = month * 30
        day = max(int(use_d), int(sys_d)) - min(int(use_d), int(sys_d))
        count = year + month + day
        if count < 1:
            return '还不到一天哦!'
        return '已经有%s天了！' % count
