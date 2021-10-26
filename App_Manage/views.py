from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.conf import settings as sys
import os
import json
from App_Blog.models import Article, Tags, Category, LeaveMsg
from App_Essay.models import Essay


def has_permission(request):
    if request.user.is_superuser:
        return True
    return False


class ArticleManage(View):
    # 文章管理
    def get(self, request):
        if has_permission(request):
            # 分类和标签
            tagsObj = Tags.objects.all()
            cateObj = Category.objects.all()
            # 分页
            page = request.GET.get('page')
            article_obj = Article.objects.all()
            paginator = Paginator(article_obj, 8)
            pageObj = paginator.get_page(page)
            return render(request, 'managehtml/article.html', locals())
        return redirect(reverse('blog:home'))

    def post(self, request):
        if has_permission(request):
            print('POAT请求到来！')
            post_type = request.GET.get('type')
            if post_type == 'add':
                title = request.POST.get('article_title')
                tag = request.POST.get('tags')
                cate = request.POST.get('category')
                body = request.POST.get('article_body')
                desc = body[3:-3]
                if all([title, tag, cate, body]):
                    Article.objects.create()
            elif post_type == 'edit':
                print('收到编辑请求')
            elif post_type == 'delete':
                print('收到删除请求')
            return None
        return redirect(reverse('blog:home'))


class TagsManage(View):
    # 标签管理
    def get(self, request):
        if has_permission(request):
            return None
        return redirect(reverse('blog:home'))

    def post(self, request):
        if has_permission(request):
            return None
        return redirect(reverse('blog:home'))


class CategoryManage(View):
    # 分类管理
    def get(self, request):
        if has_permission(request):
            return None
        return redirect(reverse('blog:home'))

    def post(self, request):
        if has_permission(request):
            return None
        return redirect(reverse('blog:home'))


class EssayManage(View):
    # 随笔管理
    def get(self, request):
        if has_permission(request):
            return None
        return redirect(reverse('blog:home'))

    def post(self, request):
        if has_permission(request):
            return None
        return redirect(reverse('blog:home'))


class LeaveMsgManage(View):
    # 留言管理
    def get(self, request):
        if has_permission(request):
            return None
        return redirect(reverse('blog:home'))

    def post(self, request):
        if has_permission(request):
            return None
        return redirect(reverse('blog:home'))


class UserManage(View):
    # 用户管理
    def get(self, request):
        if has_permission(request):
            return None
        return redirect(reverse('blog:home'))

    def post(self, request):
        if has_permission(request):
            return None
        return redirect(reverse('blog:home'))


class AdminLogin(View):
    def get(self, request):
        return render(request, 'managehtml/admin_login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        authUser = auth.authenticate(username=username, password=password)
        if authUser:
            auth.login(request, authUser)
            if has_permission(request):
                return redirect(reverse('manage:article_manage'))
            else:
                return redirect(reverse('blog:home'))
        else:
            return render(request, 'managehtml/admin_login.html', {'error_msg': '对不起您的输入有误,请重试!'})
