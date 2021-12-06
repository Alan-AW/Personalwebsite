from django.shortcuts import render
from django.views import View
from App_Essay.models import *
from App_Manage.middware.get_city import city as cy


class EssayView(View):
    """
    随笔视图
    """
    def get(self, request):
        essayObj = Essay.objects.all()
        city = cy
        return render(request, 'essay/essay.html', locals())
