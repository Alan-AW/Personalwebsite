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
from App_Blog.models import Article, Tags, Category, LeaveMsg
from App_Essay.models import Essay


def has_permission(request):
    if request.user.is_superuser:
        return True
    return False


class ArticleManage(View):
    def __init__(self):
        self.tagsObj = Tags.objects.all()
        self.cateObj = Category.objects.all()
        self.edit_dict = None

    def get_page_obj(self, request):
        # 分页
        page = request.GET.get('page')
        article_obj = Article.objects.all()
        paginator = Paginator(article_obj, 20)
        pageObj = paginator.get_page(page)
        return pageObj

    # 文章管理
    def get(self, request):
        if has_permission(request):
            # 分类和标签
            tagsObj = self.tagsObj
            cateObj = self.cateObj
            edit_dict = self.edit_dict
            pageObj = self.get_page_obj(request)
            return render(request, 'managehtml/article.html', locals())
        return redirect(reverse('blog:home'))

    def post(self, request):
        if has_permission(request):
            post_type = 'add'
            if post_type:
                title = request.POST.get('article_title')
                tag_id = request.POST.get('tags')
                cate = request.POST.get('category')
                body = request.POST.get('article_body')
                status = False
                tagsObj = self.tagsObj
                cateObj = self.cateObj
                pageObj = self.get_page_obj(request)
                if all([title, tag_id, cate, body]):
                    soup = BeautifulSoup(body, 'html.parser')
                    # 非法标签删除操作 防止XSS攻击
                    for html_tag in soup.find_all():
                        if html_tag.name == 'script':
                            html_tag.decompose()
                    desc = soup.text[0:150]  # 文章简介描述信息
                    new_body = str(soup)  # 文章内容
                    new_article_obj = Article.objects.create(author_id=request.user.pk,
                                                             title=title,
                                                             desc=desc,
                                                             body=new_body,
                                                             category_id=cate,
                                                             )
                    new_article_obj.tags.add(tag_id)
                    # tag = Tags.objects.filter(id=tag_id).first()
                    # new_article_obj.tags.add(tag)
                    status = True
                    status_msg = 'success'
                    return render(request, 'managehtml/article.html', locals())
                else:
                    status_msg = 'error'
                    return render(request, 'managehtml/article.html', locals())
            if request.is_ajax():
                ajax_type = request.POST.get('ajax_type')
                article_id = request.POST.get('pk')
                if ajax_type == 'delete':
                    Article.objects.filter(id=article_id).first().delete()
                    return HttpResponse(json.dumps('success'))
                if ajax_type == 'change':
                    article_obj = Article.objects.filter(id=article_id).first()
                    self.edit_dict = {
                        'title': article_obj.title,
                        'body': article_obj.body,
                        'category': article_obj.category
                    }
                    return HttpResponse(json.dumps('success'))
            else:
                cnm = '大佬不要攻击我!'
                return HttpResponse(json.dumps(cnm))
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
