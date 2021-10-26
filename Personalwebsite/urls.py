from django.contrib import admin
from django.urls import path, re_path, include
from App_Blog.views import Welcome, Fishing, CoreBall, Dog
from django.views import static  # 新增
from django.conf import settings  # 新增
from django.conf.urls import url  # 新增
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('', Welcome.as_view(), name='welcome'),
    path('fishing/', Fishing.as_view(), name='fishing'),
    path('coreball/', CoreBall.as_view(), name='coreball'),
    path('dogs/', Dog.as_view(), name='dogs'),
    path('blog/', include(('App_Blog.urls', 'blog'), namespace='blog')),  # 主页面
    path('users/', include(('App_Users.urls', 'users'), namespace='users')),  # 用户
    path('comment/', include(('APP_Comment.urls', 'comment'), namespace='comment')),  # 评论
    path('essay/', include(('App_Essay.urls', 'essay'), namespace='essay')),  # 随笔
    path('site/manage/', include(('App_Manage.urls', 'manage'), namespace='manage')),  # 后台管理

]

handler403 = "App_Blog.views.page_403"
handler404 = "App_Blog.views.page_404"

'''
全局url路由错误配置方法：
    
    1.关闭DEBUG
        DEBUG = False
    
    2.在根URL：handler404 = 'AppName.views.page_404'
    3.在AppName的views.py
        def page_404(request, exception):
            return render(request, '404.html')
    **-其他参数错误一样可以使用这个方法自定义 -- “ 400、500、403...
    
*****修改了DEBUG = False之后会造成static无法加载的情况**********
修改如下：
    1． 首先修改App setting.py文件
        STATIC_URL = '/static/'
        STATIC_ROOT = 'static' ## 新增行
        STATICFILES_DIRS = [
          os.path.join(BASE_DIR, '/static/'), ##修改地方
        ]
    2． 修改urls.py
        from django.views import static ##新增
        from django.conf import settings ##新增from django.conf.urls import url ##新增

        urlpatterns = [
          path('', include('user.urls')),  
        　##　以下是新增
          url(r'^static/(?P<path>.*)$', static.serve,
              {'document_root': settings.STATIC_ROOT}, name='static'),
        ]
    
    
    到这里再运行应该是可以了，如果还有报STATIC_ROOT错。如果是下面的提示，请修改参见第一点的。

    ERRORS: ?: 
    (staticfiles.E002) The STATICFILES_DIRS setting 
    should not contain the STATIC_ROOT setting.
    
    System check identified 1 issue (0 silenced)
    . 
    os.path.join(BASE_DIR, '/static/'), #多加了/

'''
