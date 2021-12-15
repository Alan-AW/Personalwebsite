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
        icp_code = sys.ICP_CODE
        qq_user_nickname = request.GET.get('qq_nickname')
        qq_user_avata = request.GET.get('qq_avatar')
        # qq_user_nickname = '123456789123456789'
        # qq_user_avata = 'data:image/jpeg;base64,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'
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
