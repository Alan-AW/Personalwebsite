from django.urls import path, re_path
from App_Essay.views import EssayView

app_name = 'essay'
urlpatterns = [
    path('detail/', EssayView.as_view(), name='essay'),
]
