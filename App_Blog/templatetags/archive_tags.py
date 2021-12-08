from django import template
from django.db.models import Count
from App_Blog.models import *

register = template.Library()


@register.inclusion_tag('blog/archive_msg.html')
def get_archive_style():
    category = Category.objects.values('pk').annotate(c=Count('article__title')).values_list('title', 'c')
    tags = Tags.objects.values('pk').annotate(c=Count('article')).values_list('title', 'c')
    return locals()

