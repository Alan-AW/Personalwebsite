from django.shortcuts import render, redirect, HttpResponse, reverse
from django.views import View
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.db.models import F
from django.db import transaction
from django.core.paginator import Paginator
from django.core.mail import send_mail
import json
import threading
from App_Blog.models import *
from django.conf import settings as sys
from APP_Comment.models import Comment
from App_Users.models import OAuthRelationShip


class Welcome(View):
    def get(self, request):
        return render(request, 'blog/welcome.html')


class Home(View):
    """
    网站首页视图
    """

    def get(self, request, **kwargs):
        # 查询所有的文章传递给前端做展示
        page = request.GET.get('page')
        user = request.user
        articleList = Article.objects.all()
        if kwargs:
            condition = kwargs['condition']
            params = kwargs['params']
            if condition == 'category':
                articleList = articleList.filter(category__title=params)
            else:
                articleList = articleList.filter(tags__title=params)
            if not articleList:
                return render(request, '404.html')
        # 归档
        # 日期分组:-----** 移除该鸡肋功能 **-----
        # dateList = Article.objects.extra(select={'monthDate': 'date_format(created_time,"%%Y/%%m")'}).values('monthDate').annotate(c=Count('id')).values_list('monthDate', 'c')
        # 解释： 在 文章表 的 所有字段中注入一个字段 month 用日期进行过滤出格式 年月 以这个 month 字段进行排序 并且统计当前字段的 id 数量为 c 值，最终输出 该字段的格式 month 和统计的值 c
        # django 自带的日期分组查询:
        # 原理同上，调用了一个函数进行切割!!注意：该方法需要设置时区
        # dateList = Article.objects.annotate(month=TruncMonth('created_time')).values('month').annotate(c=Count('id')).values('month','c')
        # 分页
        paginator = Paginator(articleList, 10)  # Show 10 contacts per page.
        pageObj = paginator.get_page(page)
        icp_code = sys.ICP_CODE  # ICP备案信息
        # 获取用户头像和昵称信息
        qq_user_nickname = request.GET.get('qq_nickname')
        qq_user_avatar = request.GET.get('qq_avatar')
        if all([qq_user_nickname, qq_user_avatar]):
            return render(request, 'blog/home.html', locals())
        if not all([qq_user_nickname, qq_user_avatar]):
            if user:
                try:
                    qq_user_obj = OAuthRelationShip.objects.filter(user=user).first()
                except Exception:
                    qq_user_obj = None
                if qq_user_obj:
                    qq_user_nickname = qq_user_obj.nickname
                    qq_user_avatar = qq_user_obj.avatar
        return render(request, 'blog/home.html', locals())


class ArticleDetail(View):
    """
    文章详情
    """

    def get(self, request, articleId):
        hasArticle = Article.objects.filter(id=articleId)
        articleObj = Article.objects.filter(id=articleId).first()
        if not articleObj:
            return render(request, '404.html')
        hasArticle.update(views=F('views') + 1)
        commentObj = Comment.objects.filter(articleId=articleId)
        commentList = commentObj.filter(parentId=None)
        # 上一篇
        ltArticle = Article.objects.filter(id__lt=articleId).all().order_by("-id").first()
        # 下一篇
        gtArticle = Article.objects.filter(id__gt=articleId).all().order_by("id").first()
        icp_code = sys.ICP_CODE
        return render(request, 'blog/articleDetail.html', locals())

    def post(self, request, articleId):
        # 点赞处理
        if request.is_ajax():
            is_Login = json.loads(request.POST['isLogin'])  # 传过来的是布尔值
            user = request.POST['user']
            if user == 'get_ip_addrs':
                user = request.META.get('REMOTE_ADDR')
            articleId = request.POST['articleId']
            articleObj = Article.objects.filter(id=articleId)
            responseObj = {'success': False}
            if is_Login:
                is_grated = Great.objects.filter(user_id=user, article_id=articleId).first()
                login = True
            else:
                is_grated = Great.objects.filter(userIp=user, article_id=articleId).first()
                login = False
            if is_grated:
                return HttpResponse(json.dumps(responseObj))
            else:
                try:
                    with transaction.atomic():
                        Great.objects.create(user_id=user, article_id=articleId, isUp=True) if login else \
                            Great.objects.create(userIp=user, article_id=articleId, isUp=True)
                        articleObj.update(greatCount=F('greatCount') + 1)
                    responseObj['success'] = True
                except:
                    responseObj['serverOver'] = True
            return HttpResponse(json.dumps(responseObj))
        else:
            cnm = '禁止爬虫'
            return HttpResponse(json.dumps(cnm))


class LeaveMsgView(View):
    """
    留言板
    """

    def get(self, request):
        leaveObj = LeaveMsg.objects.all()
        allLeave = leaveObj.filter(parent=None)
        # 后期视情况增加分页
        leaveCount = leaveObj.count()  # 统计留言总数
        return render(request, 'other/leave.html', locals())

    def post(self, request):
        if request.is_ajax():
            nickname = request.POST['nickname']
            emailAttr = request.POST['emailAttr']
            site = request.POST['site']
            browserId = request.POST['browserId']
            city = request.POST['city']
            content = request.POST['content'][:-2]
            status = {'success': False}
            # 开启事物，同步数据
            try:
                LeaveMsg.objects.create(name=nickname, content=content, browserId=browserId, site=site, email=emailAttr,
                                        city=city)
                status['success'] = True
            except:
                return HttpResponse(json.dumps(status))
            # 另开线程发送通知邮件
            t = threading.Thread(target=send_mail, args=(
                '留言板新增一条留言',
                content + '请点击查看内容：www.missyouc.cn/blog/leavemessage/',
                sys.EMAIL_HOST_USER,
                [sys.EMAIL_SELF_ATTR]
            ))
            t.start()
            # 返回信息
            return HttpResponse(json.dumps(status))
        else:
            cnm = '本次访问存在违规操作，已被系统标记！'
            return HttpResponse(json.dumps(cnm))


class AddNewLeave(View):
    def post(self, request):
        if request.is_ajax():
            status = {}
            rootId = request.POST['rootId']
            name = request.POST['name']
            city = request.POST['city']
            browserId = request.POST['browserId']
            email = request.POST['email']
            site = request.POST['site']
            content = request.POST['content']
            leaveObj = LeaveMsg.objects.filter(id=rootId).first()
            try:
                root_id = leaveObj.root.id
                has_sql_root = True
            except:
                root_id = rootId
                has_sql_root = False
            parentId = rootId
            rootUser = leaveObj.name
            try:
                LeaveMsg.objects.create(name=name, content=content, browserId=browserId, site=site, email=email,
                                        parent_id=parentId, city=city, replayTo_id=rootId, root_id=root_id)
                status['success'] = True
            except:
                status['success'] = False
                return HttpResponse(json.dumps(status))
            # 开线程-发邮件
            if has_sql_root:
                user_email = LeaveMsg.objects.filter(id=root_id).first().email
                if user_email:
                    t = threading.Thread(target=send_mail, args=(
                        '您在“花有重开日，人无再少年”的网站留言收到了新的回复',
                        content + '请点击查看内容：www.xumeijie.com/blog/leavemessage/',
                        sys.EMAIL_HOST_USER,
                        [email]
                    ))
                    t.start()
            # 构建出返回前端的数据
            status['replyToUser'] = rootUser
            status['rootId'] = root_id
            return HttpResponse(json.dumps(status))
        else:
            cnm = '您的本次操作存在违规操作，已被系统标记！'
            return HttpResponse(json.dumps(cnm))


class EternalLove(View):
    def get(self, request):
        is_her = request.session.get(sys.ETERNAL_KEY)
        if is_her:
            return render(request, 'blog/eternal.html')
        return redirect(reverse('blog:about'))

    def post(self, request):
        if request.is_ajax():
            name = request.POST.get('name')
            close = request.POST.get('close')
            if close:
                request.session[sys.ETERNAL_KEY] = False
            if name == sys.ETERNAL_NAME:
                request.session[sys.ETERNAL_KEY] = True
                return HttpResponse(json.dumps({'is_her': True}))
            return HttpResponse(json.dumps({'is_her': False}))
        return HttpResponse(json.dumps('你不是我要等的人!'))


class EnShi(View):
    def get(self, request):
        return render(request, 'blog/enshi.html')


class About(View):
    def get(self, request):
        return render(request, 'other/about.html')


class Ali(View):
    def get(self, request):
        return render(request, 'other/ali.html')


class Fishing(View):
    def get(self, request):
        return render(request, 'other/Fishing.html')


class CoreBall(View):
    def get(self, request):
        return render(request, 'other/jfcz.html')


class Dog(View):
    def get(self, request):
        return render(request, 'other/Dog.html')


def page_404(request, exception):
    return render(request, '404.html')


def page_403(request, exception):
    return render(request, '404.html')
