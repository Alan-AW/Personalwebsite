from django.db import models
from django.contrib.auth.models import User


class Tags(models.Model):
    """
    文章标签
    """
    title = models.CharField(max_length=10)

    class Meta:
        db_table = 'Tags'
        verbose_name = "标签"

    def __str__(self):
        return self.title


class Category(models.Model):
    """
    文章分类
    """
    title = models.CharField(max_length=10)

    class Meta:
        db_table = 'Category'
        verbose_name = "分类"

    def __str__(self):
        return self.title


class Article(models.Model):
    """
    文章表
    """
    author = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    title = models.CharField(max_length=30, verbose_name='标题', )
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now=True)
    desc = models.CharField(max_length=70, verbose_name='摘要')
    body = models.TextField()
    views = models.PositiveIntegerField(default=0, editable=False)
    category = models.ForeignKey(Category, verbose_name="分类", on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags, verbose_name="标签", blank=True)
    greatCount = models.IntegerField(default=0)  # 点赞数
    commentCount = models.IntegerField(default=0)  # 评论数

    class Meta:
        db_table = 'Article'
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        ordering = ["created_time"]

    def __str__(self):
        return self.title


class Great(models.Model):
    """
    点赞表
    """
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)  # to='表名'  可以简写成  '表名'
    article = models.ForeignKey(Article, null=True, on_delete=models.CASCADE)  # 文章
    userIp = models.GenericIPAddressField(max_length=15, null=True, verbose_name='IP')
    isUp = models.BooleanField(default=True)

    class Meta:
        unique_together = [  # 避免一模一样的文章和作者信息重复
            ('article', 'user')
        ]
        db_table = 'Great'
        verbose_name = '点赞'


class LeaveMsg(models.Model):
    """
    留言板
    """
    name = models.CharField(null=True, verbose_name='昵称', max_length=20)
    email = models.EmailField(null=True, verbose_name='邮箱', )
    createTime = models.DateField(verbose_name='留言时间', auto_now_add=True)
    content = models.CharField(verbose_name='内容', max_length=500)
    site = models.CharField(verbose_name='网址', null=True, max_length=30)
    browserId = models.CharField(verbose_name='浏览器标识', max_length=20, null=True)
    city = models.CharField(verbose_name='城市', max_length=10)
    root = models.ForeignKey('self', related_name='rootleave', null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='parentleave', null=True, on_delete=models.CASCADE)
    replayTo = models.ForeignKey('self', related_name='replies', null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'LeaveMsg'
        verbose_name = '留言板'

    def __str__(self):
        return self.content
