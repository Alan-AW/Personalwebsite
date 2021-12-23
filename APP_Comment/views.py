from django.shortcuts import render, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import F
from django.views import View
from Personalwebsite import settings as sys
from django.core.mail import send_mail
import json, threading
from APP_Comment.models import *
from App_Blog.models import Article


class AddComment(LoginRequiredMixin, View):
    def get(self, request):
        return HttpResponse(json.dumps('fuck you!'))

    def post(self, request):
        if request.is_ajax():
            userId = request.POST['userId']
            articleId = request.POST['articleId']
            content = request.POST['content'][:-2]
            browserId = request.POST['browserId']
            article_obj = Article.objects.filter(id=articleId)
            response = {}
            try:
                with transaction.atomic():
                    Comment.objects.create(user_id=userId, articleId_id=articleId, body=content, browserId=browserId)
                    article_obj.update(commentCount=F('commentCount') + 1)
                response['successComment'] = True
            except Exception:
                response['successComment'] = False
            t = threading.Thread(target=send_mail, args=(
                '文章《%s》新增一条评论' % article_obj.first().title,
                content,
                sys.EMAIL_HOST_USER,
                [sys.EMAIL_SELF_ATTR])
                                 )
            t.start()
            return HttpResponse(json.dumps(response))
        else:
            cnm = '您的本次请求存在违法信息，已被系统标记！'
            return HttpResponse(json.dumps(cnm))


class AddReply(LoginRequiredMixin, View):
    def post(self, request):
        if request.is_ajax():
            replyPk = request.POST['replyPk']
            userId = request.user.pk
            articleId = request.POST['articleId']
            content = request.POST['content'][:-2]
            browserId = request.POST['browserId']
            status = {}
            if all([replyPk, userId, articleId, content, browserId]):
                article_obj = Article.objects.filter(id=articleId)
                # 查询到当前被评论的这条评论
                replyObj = Comment.objects.filter(id=replyPk).first()
                # 获取到他的根评论id
                try:
                    rootId = replyObj.root.id
                except:
                    rootId = replyPk
                parentId = replyPk
                # 获取到该条评论的用户名
                rootUser = replyObj.user.username
                rootUserPk = replyObj.user.id
                # 开启事物，同步数据
                try:
                    with transaction.atomic():
                        Comment.objects.create(user_id=userId,
                                               replayTo_id=rootUserPk,
                                               root_id=rootId,
                                               parentId_id=parentId,
                                               articleId_id=articleId,
                                               body=content,
                                               browserId=browserId)
                        article_obj.update(commentCount=F('commentCount') + 1)
                    status['success'] = True
                except:
                    status['success'] = False
                    return HttpResponse(json.dumps(status))
                # 构建出返回前端的数据
                status['replyToUser'] = rootUser
                status['rootId'] = rootId
            else:
                status['success'] = False
            return HttpResponse(json.dumps(status))
        else:
            cnm = '您的本次操作属于违规操作，已被系统标记。'
            return HttpResponse(json.dumps(cnm))


def send_email(email, request):
    subject = '个人博客找回密码'
    html_message = f"<p>可爱的用户：</p>&emsp;您好！此链接用于用户找回密码，请点击链接：" \
                   f"<a href='http://127.0.0.1:8000/retrieve_pwd?code='>找回密码</a>，<br/>" \
                   f"如果链接不能点击，请复制：http://127.0.0.1:8000/retrieve_pwd?code=<br/>" \
                   f"个人博客团队"
    'https://blog.csdn.net/CurtainOfNight/article/details/104053669'
    result = send_mail(subject, '', sys.EMAIL_HOST_USER, [email, ], html_message=html_message)
    return result
