from django.conf import settings as sys
from urllib.request import urlopen
from urllib.parse import urlencode
import json


def get_qq_user_msg(access_token, openid):
    # 获取用户QQ信息
    params = {
        'access_token': access_token,
        'oauth_consumer_key': sys.QQ_APP_ID,
        'openid': openid,
    }
    response = urlopen('https://graph.qq.com/user/get_user_info?' + urlencode(params))
    data = json.loads(response.read().decode('utf8'))
    qq_avatar = data.get('figureurl_qq_2').replace('http', 'https')
    params = {
        'qq_nickname': data.get('nickname'),  # QQ用户昵称
        'qq_avatar': qq_avatar  # 100*100头像
    }
    return params
