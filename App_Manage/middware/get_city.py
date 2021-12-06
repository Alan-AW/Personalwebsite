from Personalwebsite.settings import BMAP_URL
import requests
import json


def get_city():
    url = BMAP_URL
    rsp = requests.get(url)
    ret = json.loads(rsp.content)
    user_city = ret.get('content').get('address_detail').get('city')
    return str(user_city)


city = get_city()
