from django.urls import path,re_path
from App_Users.views import *


app_name = 'users'
urlpatterns = [
    path('login/', Signin.as_view(), name='signin'),
    path('logout/', Logout.as_view(), name='logout'),
    path('forgotPwd/', ForgotPwd.as_view(), name='forgotPwd'),
    path('login_by_qq', QQLogin.as_view(), name='qq_login'),
    path('user_detail/', UserDetail.as_view(), name='user_detail'),
]
