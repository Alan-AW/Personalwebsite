from django.urls import path,re_path
from .views import *

app_name = 'comment'
urlpatterns = [
    path('addComment/', AddComment.as_view(), name='addComment'),  # 评论路由
    path('addReply/', AddReply.as_view(), name='addReply')
]
