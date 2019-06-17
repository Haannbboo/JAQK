import random
import hashlib
import urllib
import json
import requests


def _t_util(text, t, f):
    # if not (t in Lans().values() and f in Lans().values()):
    #    raise ValueError("Inaapropriate language set, use function Lans() to see the abbreviations of languages")
    # Using Baidu translate API
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    app_id = '20190321000279637'
    secretKey = 'mCoDy3N0ANeB7MVtUsDT'  # My own
    salt = random.randint(12345, 98765)

    temp = app_id + text + str(salt) + secretKey
    sign = hashlib.md5(temp.encode()).hexdigest()

    r_url = url + '?q=' + urllib.parse.quote(text) + '&from=' + f + '&to=' + t + '&appid=' + app_id + '&salt=' + str(
        salt) + '&sign=' + sign

    r = requests.get(r_url, timeout=7).content.decode('utf-8')
    data = json.loads(r)
    result = str(data['trans_result'][0]['dst'])

    return result


def _translate(text, t='en'):
    if t == 'en':
        return text
    trans = _t_util(text, t, f='en')
    return trans
