from django.conf import settings as sys
import requests
import json


def get_city():
    url = sys.BMAP_URL
    rsp = requests.get(url)
    ret = json.loads(rsp.content)
    user_city = ret.get('content').get('address_detail').get('city')
    return user_city


city = get_city()
