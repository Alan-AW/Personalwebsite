from django.shortcuts import render
from django.views import View
from .models import *


class EssayView(View):
    """
    随笔视图
    """
    def get(self, request):
        essayObj = Essay.objects.all()
        return render(request,'essay/essay.html',locals())

