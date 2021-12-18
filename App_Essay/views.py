from django.shortcuts import render
from django.views import View
from App_Essay.models import *
from django.conf import settings as sys
from App_Users.models import OAuthRelationShip


class EssayView(View):
    """
    随笔视图
    """
    def get(self, request):
        essayObj = Essay.objects.all().order_by('-id')
        icp_code = sys.ICP_CODE
        user = request.user
        if user:
            try:
                qq_user_obj = OAuthRelationShip.objects.filter(user=user).first()
            except Exception:
                qq_user_obj = None
            if qq_user_obj:
                qq_user_nickname = qq_user_obj.nickname
                qq_user_avatar = qq_user_obj.avatar
        return render(request, 'essay/essay.html', locals())
