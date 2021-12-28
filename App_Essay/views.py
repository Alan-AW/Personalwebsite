from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from django.conf import settings as sys
from App_Essay.models import *
from App_Users.models import OAuthRelationShip


class EssayView(View):
    """
    随笔视图
    """
    def get(self, request):
        page = request.GET.get('page')
        essayObj = Essay.objects.all().order_by('-id')
        icp_code = sys.ICP_CODE
        user = request.user
        paginator = Paginator(essayObj, 5)
        page_obj = paginator.get_page(page)
        if user:
            try:
                qq_user_obj = OAuthRelationShip.objects.filter(user=user).first()
            except Exception:
                qq_user_obj = None
            if qq_user_obj:
                qq_user_nickname = qq_user_obj.nickname
                qq_user_avatar = qq_user_obj.avatar
        return render(request, 'essay/essay.html', locals())
