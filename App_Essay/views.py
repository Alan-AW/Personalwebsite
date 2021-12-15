from django.shortcuts import render
from django.views import View
from App_Essay.models import *
from django.conf import settings as sys


class EssayView(View):
    """
    随笔视图
    """
    def get(self, request):
        essayObj = Essay.objects.all()
        icp_code = sys.ICP_CODE
        return render(request, 'essay/essay.html', locals())
