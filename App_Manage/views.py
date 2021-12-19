import os
import json
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.conf import settings as sys
from bs4 import BeautifulSoup
from App_Users.models import OAuthRelationShip
from APP_Comment.models import Comment
from App_Blog.models import Article, Tags, Category, LeaveMsg
from App_Essay.models import Essay


def get_article_desc(body):
    soup = BeautifulSoup(body, 'html.parser')
    # 非法标签删除操作 防止XSS攻击
    for html_tag in soup.find_all():
        if html_tag.name == 'script':
            html_tag.decompose()
    desc = soup.text[0:70]
    new_body = str(soup)
    return [desc, new_body]


def get_page_obj(request, model_obj, num):
    # 分页
    page = request.GET.get('page')
    model = model_obj.objects.all()
    paginator = Paginator(model, num)
    pageObj = paginator.get_page(page)
    return pageObj


class SiteManage(View):
    def get(self, request):
        article_count = Article.objects.all().count()
        comment_count = Comment.objects.all().count()
        tags_count = Tags.objects.all().count()
        cate_count = Category.objects.all().count()
        essay_count = Essay.objects.all().count()
        leave_count = LeaveMsg.objects.all().count()
        users_count = User.objects.all().count()
        return render(request, 'managehtml/manage_home.html', locals())


class ArticleManage(View):
    def __init__(self):
        self.tagsObj = Tags.objects.all()
        self.cateObj = Category.objects.all()
        self.edit_dict = None

    # 文章管理
    def get(self, request):
        # 分类和标签
        tagsObj = self.tagsObj
        cateObj = self.cateObj
        edit_dict = self.edit_dict
        pageObj = get_page_obj(request, Article, 20)
        return render(request, 'managehtml/article.html', locals())

    def post(self, request):
        if request.is_ajax():
            ajax_type = request.POST.get('ajax_type')
            article_id = request.POST.get('pk')
            if ajax_type == 'delete':
                Article.objects.filter(id=article_id).first().delete()
                return HttpResponse(json.dumps('success'))
        else:
            title = request.POST.get('article_title')
            tag_id = request.POST.getlist('tags')
            cate = request.POST.get('category')
            body = request.POST.get('article_body')
            status = False
            tagsObj = self.tagsObj
            cateObj = self.cateObj
            pageObj = get_page_obj(request, Article, 20)
            if all([title, tag_id, cate, body]):
                param = get_article_desc(body)
                desc = param[0]
                new_body = param[1]
                new_article_obj = Article.objects.create(author_id=request.user.pk,
                                                         title=title,
                                                         desc=desc,
                                                         body=new_body,
                                                         category_id=cate,
                                                         )
                new_article_obj.tags.add(*tag_id)
                # tag = Tags.objects.filter(id=tag_id).first()
                # new_article_obj.tags.add(tag)
                status = True
                status_msg = 'success'
                return render(request, 'managehtml/article.html', locals())
            else:
                status_msg = 'error'
                return render(request, 'managehtml/article.html', locals())


class ChangeArticle(View):
    def get(self, request, pk):
        articleObj = Article.objects.filter(id=pk).first()
        if articleObj:
            title = articleObj.title
            tagsObj = Tags.objects.all()
            cateObj = Category.objects.all()
            body = articleObj.body
            return render(request, 'managehtml/change_article.html', locals())
        return HttpResponse('参数错误，请检查后重试!')

    def post(self, request, article_id):
        articleObj = Article.objects.filter(id=article_id).first()
        title = request.POST.get('article_title')
        body = request.POST.get('article_body')
        tags = request.POST.getlist('tags')
        category = request.POST.get('category') or articleObj.category.pk
        if all([articleObj, title, body, tags, category]):
            param = get_article_desc(body)
            desc = param[0]
            new_body = param[1]
            Article.objects.filter(pk=article_id).update(title=title, desc=desc, body=new_body, category=category)
            tag_obj = Tags.objects.filter(id__in=tags)
            for i in tag_obj:
                articleObj.tags.add(i)
            return redirect(reverse('manage:article_manage'))
        return HttpResponse('参数缺失或者不完整，请检查后重试!')


class TagsManage(View):
    def get_queryset(self):
        return Tags.objects.all()

    # 标签管理
    def get(self, request):
        tags = self.get_queryset()
        return render(request, 'managehtml/tags.html', locals())

    def post(self, request):
        if request.is_ajax():
            post_type = request.POST.get('post_type')
            if post_type == 'edit_tags':
                tags_pk = request.POST.get('pk')
                title = request.POST.get('title')
                Tags.objects.filter(id=tags_pk).update(title=title)
                return HttpResponse(json.dumps('success'))
            return HttpResponse(json.dumps('error'))
        tags = self.get_queryset()
        post_type = request.GET.get('type')
        if post_type == 'delete':
            id_list = request.POST.getlist('pk')
            try:
                Tags.objects.filter(id__in=id_list).delete()
                make_status = {'success': True}
            except ModuleNotFoundError:
                make_status = {'success': False}
        if post_type == 'add':
            title = request.POST.get('title')
            if title:
                Tags.objects.create(title=title)
                make_status = {'success': True}
            else:
                make_status = {'success': False}
        return render(request, 'managehtml/tags.html', locals())


class CategoryManage(View):
    # 分类管理
    def get_queryset(self):
        return Category.objects.all()

    def get(self, request):
        cateObj = self.get_queryset()
        return render(request, 'managehtml/category.html', locals())

    def post(self, request):
        cateObj = self.get_queryset()
        post_type = request.GET.get('type')
        if post_type == 'delete':
            id_list = request.POST.getlist('pk')
            try:
                Category.objects.filter(id__in=id_list).delete()
                make_status = {'success': True}
            except ModuleNotFoundError:
                make_status = {'success': False}
        if post_type == 'add':
            title = request.POST.get('title')
            if title:
                Category.objects.create(title=title)
                make_status = {'success': True}
            else:
                make_status = {'success': False}
        return render(request, 'managehtml/category.html', locals())


class EssayManage(View):
    # 随笔管理
    def get_queryset(self):
        return Essay.objects.all()

    def get(self, request):
        all_essay = self.get_queryset()
        return render(request, 'managehtml/essay.html', locals())

    def post(self, request):
        if request.is_ajax():
            response = dict()
            pk = request.POST.get('pk')
            state = request.POST.get('state')
            if state == 'del':
                try:
                    Essay.objects.get(id=pk).delete()
                    response['is_true'] = True
                except Exception:
                    response['is_true'] = False
                ret = json.dumps(response)
            else:
                response['is_true'] = '请求参数校验错误!'
                ret = json.dumps(response)
            return HttpResponse(ret)
        title = request.POST.get('title')
        body = request.POST.get('body')
        if all([title, body]):
            try:
                Essay.objects.create(title=title, body=body)
            except Exception:
                error_msg = '服务器错误，稍后再试！'
            all_essay = self.get_queryset()
            return render(request, 'managehtml/essay.html', locals())
        else:
            error_msg = '参数不完整，检查一下。'
            all_essay = self.get_queryset()
            return render(request, 'managehtml/essay.html', locals())


class LeaveMsgManage(View):
    # 留言管理
    def __init__(self):
        self._count = LeaveMsg.objects.all().count()

    def get(self, request):
        page_obj = get_page_obj(request, LeaveMsg, 20)
        count = self._count
        return render(request, 'managehtml/leave.html', locals())

    def post(self, request):
        pk_list = request.POST.getlist('pk_list')
        page_obj = get_page_obj(request, LeaveMsg, 20)
        count = self._count
        try:
            LeaveMsg.objects.filter(id__in=pk_list).delete()
        except Exception:
            error_msg = '操作失败!'
        return render(request, 'managehtml/leave.html', locals())


class UserManage(View):
    # 用户管理
    def get(self, request):
        # 所有用户统计数据
        userObj = User.objects.all()
        userCount = userObj.count()
        oauthObj = OAuthRelationShip.objects.all()
        oauthCount = oauthObj.count()
        register_count = userCount - oauthCount

        # 用户互动数据
        all_leave = LeaveMsg.objects.all()
        all_comment = Comment.objects.all()
        user_manage = []
        comment_count = 0
        leave_count = 0
        for user in userObj:
            user_dict = {'user_id': user.id,
                         'username': user.username,
                         'date_joined': user.date_joined,
                         'last_login': user.last_login}
            if user.is_superuser:
                user_dict['super'] = True
            else:
                user_dict['super'] = False
            for oauth in oauthObj:
                if oauth.user == user:
                    user_dict['qq_avatar'] = oauth.avatar
                    user_dict['qq_nickname'] = oauth.nickname
            for comment in all_comment:
                if comment.user == user:
                    comment_count += 1
                    user_dict['comment_count'] = comment_count
            for leave in all_leave:
                if leave.name == user.username:
                    leave_count += 1
                    user_dict['leave_count'] = leave_count
            user_manage.append(user_dict)

        return render(request, 'managehtml/users.html', locals())

    def post(self, request):
        # 获取请求中所有的pk
        user_pk = request.POST.getlist('user_pk')
        # 获取数据库中所有超级用户的pk
        all_super = User.objects.filter(is_superuser=True)
        super_pk = list()
        for item in all_super:
            super_pk.append(item.pk)
        # 提取出不同的pk
        different_list = self.get_different_list(user_pk, super_pk)
        # 请求 > 数据库
        if len(user_pk) > all_super.count():
            # 增加超管
            add_super_obj = User.objects.get(id__in=different_list)
            add_super_obj.is_superuser = True
            add_super_obj.save()
            return self.get(request)
        # 请求 < 数据库
        if len(user_pk) < all_super.count():
            # 取消超管
            del_super_obj = User.objects.get(id__in=different_list)
            del_super_obj.is_superuser = False
            del_super_obj.save()
            return self.get(request)
        else:
            return self.get(request)

    def get_different_list(self, list1, list2):
        set1 = set([int(item) for item in list1])
        set2 = set([int(item) for item in list2])
        public = list(set1 ^ set2)
        return public


class AdminLogin(View):
    def get(self, request):
        if request.user.is_superuser:
            return redirect(reverse('manage:manage_home'))
        return render(request, 'managehtml/admin_login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        authUser = auth.authenticate(username=username, password=password)
        if authUser:
            auth.login(request, authUser)
            if request.user.is_superuser:
                return redirect(reverse('manage:manage_home'))
            else:
                return redirect(reverse('blog:home'))
        else:
            return render(request, 'managehtml/admin_login.html', {'error_msg': '对不起您的输入有误,请重试!'})
