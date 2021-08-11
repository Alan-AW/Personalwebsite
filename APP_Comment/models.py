from django.db import models
from django.contrib.auth.models import User
from App_Blog.models import Article


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.DO_NOTHING)  # 用户
    time = models.DateField(auto_now_add=True)  # 评论时间
    articleId = models.ForeignKey(Article, on_delete=models.DO_NOTHING)  # 文章
    body = models.TextField()  # 评论内容
    browserId = models.CharField(max_length=24, null=True)  # 浏览器标识
    root = models.ForeignKey('self', null=True, related_name='rootComment', on_delete=models.DO_NOTHING)  # 指向其顶级评论
    parentId = models.ForeignKey('self', null=True, related_name='parentComment', on_delete=models.DO_NOTHING)  # 父评论
    replayTo = models.ForeignKey(User, null=True, related_name='replies', on_delete=models.DO_NOTHING)  # 回复了谁

    def __str__(self):
        return self.body

    class Meta:
        verbose_name = '评论'
        db_table = 'comment'
        ordering = ['-time']
