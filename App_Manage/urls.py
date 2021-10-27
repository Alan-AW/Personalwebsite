from django.urls import path, re_path, include
from App_Manage.views import *

urlpatterns = [
    path('admin/login/', AdminLogin.as_view(), name='admin_login'),
    path('article/', ArticleManage.as_view(), name='article_manage'),
    path('tags/', TagsManage.as_view(), name='tags_manage'),
    path('category/', CategoryManage.as_view(), name='category_manage'),
    path('essay/', EssayManage.as_view(), name='essay_manage'),
    path('leave/', LeaveMsgManage.as_view(), name='leave_manage'),
    re_path('change_article/(\d+)/$', ChangeArticle.as_view(), name='change_article'),

]
