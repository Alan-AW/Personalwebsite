from django.urls import path, re_path
from App_Blog.views import *

app_name = 'blog'
urlpatterns = [
    path('about/xmj/', About.as_view(), name='about'),
    path('home/', Home.as_view(), name='home'),
    path('ali/', Ali.as_view(), name='ali'),
    path('leavemessage/', LeaveMsgView.as_view(), name='leavemsg'),
    path('addNewLeave/', AddNewLeave.as_view(), name='addNewLeave'),
    path('enshi/', EnShi.as_view(), name='enshi'),
    re_path('articles/(?P<articleId>\d+)$', ArticleDetail.as_view(), name='articles'),
    re_path('home/(?P<condition>category|tags)/(?P<params>(\w+/?\w+))$', Home.as_view())
]
