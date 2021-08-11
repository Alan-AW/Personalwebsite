from django.urls import path, re_path
from .views import *

app_name = 'essay'
urlpatterns = [
    path('detail/', EssayView.as_view(), name='essay'),
]
