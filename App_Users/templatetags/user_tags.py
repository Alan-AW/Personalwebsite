from django import template
from django.conf import settings as sys
from urllib.parse import urlencode


register = template.Library()


@register.simple_tag
def get_login_qq_url():
    params = {
        'response_type': 'code',
        'client_id': sys.QQ_APP_ID,
        'redirect_url': sys.QQ_REDIRECT_URL,
        'state': sys.QQ_STATE,
    }
    url = 'https://graph.qq.com/oauth2.0/authorize?' + urlencode(params)
    return url
