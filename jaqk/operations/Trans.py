import random
import hashlib
import urllib
import json
import requests

from ..exceptions import TransInternetError


def _t_util(text, t, f):
    # Using Baidu translation API
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    app_id = '20190321000279637'
    secretKey = 'mCoDy3N0ANeB7MVtUsDT'  # My secret key
    salt = random.randint(12345, 98765)

    temp = app_id + text + str(salt) + secretKey
    sign = hashlib.md5(temp.encode()).hexdigest()  # generate sign

    r_url = '{url}?q={text}&from={f}&to={t}&appid={appid}&salt={salt}&sign={sign}'.format(
        url=url,
        text=urllib.parse.quote(text),
        f=f, t=t, appid = app_id,
        salt=salt, sign=sign)  # create request url

    try:
        r = requests.get(r_url, timeout=5).content.decode('utf-8')
        data = json.loads(r)  # parse json
        result = str(data['trans_result'][0]['dst'])
    except requests.exceptions.ConnectionError:
        # should connect to exceptions.py
        return None

    return result


def _translate(text, t='en'):
    if t == 'en':  # no need to translate
        return text
    trans = _t_util(text, t, f='en')
    if trans is None:
        error = "Translation failed. Check your internet pleases."
        raise TransInternetError(error)
    return trans


