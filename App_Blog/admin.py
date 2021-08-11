from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Article)
admin.site.register(Tags)
admin.site.register(Category)
admin.site.register(Great)
admin.site.register(LeaveMsg)

