from django.db import models
from ckeditor.fields import RichTextField  # 后台编辑器
# from django.contrib.auth.models import User


class Essay(models.Model):
    title = models.CharField(max_length=64)
    date = models.DateField(auto_now_add=True)
    body = models.TextField()

    class Meta:
        verbose_name = '随笔'
        db_table = 'essay'

    def __str__(self):
        return self.title
