from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect, HttpResponse, reverse
import re


class Middleware(MiddlewareMixin):
    def process_request(self, request):
        current_url = request.path_info
        if current_url == reverse('manage:admin_login'):
            return None
        is_super_user = request.user.is_superuser
        mast = '^/site/manage/.*?$'
        if re.match(mast, current_url):
            if not is_super_user:
                return redirect(reverse('blog:home'))
        else:
            return None
