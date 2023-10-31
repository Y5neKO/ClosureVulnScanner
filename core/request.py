"""
@Time: 2023/10/26 20:45
@Auth: Y5neKO
@File: request.py
@IDE: PyCharm

web请求模块
"""
import random
import socket
import ssl
from urllib.parse import urlparse

import requests
from urllib3 import disable_warnings
from urllib3.util import parse_url

from core.log import *

# 随机User-Agent防检测
ua = random.choice([
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 "
    "Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 "
    "Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 "
    "Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 "
    "Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 "
    "Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 "
    "Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 "
    "Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 "
    "Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36",
    "Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 "
    "Safari/537.17",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14"])


def check_network() -> bool:
    ipaddress = socket.gethostbyname(socket.gethostname())
    if ipaddress == 'www.baidu.com':
        return False
    else:
        return True


def check_protocol(url):
    if url.startswith("http"):
        return url
    else:
        return "http://" + url


def alive(url) -> bool:
    ipaddress = socket.gethostbyname(socket.gethostname())
    if ipaddress == url:
        return False
    else:
        return True


def web_request(url, cookie=None, post=None, timeout=5000):
    if check_network():
        url = check_protocol(url)
        try:
            disable_warnings()
            session = requests.Session()
            session.verify = False  # 关闭SSL校验
            response = session.get(url, headers={"User-Agent": ua}, cookies=cookie, data=post, timeout=timeout / 1000,
                                   allow_redirects=True)
            if response.is_redirect:  # 检查是否发生重定向
                location = response.headers['Location']
                parsed_location = parse_url(location)
                if parsed_location.scheme == 'http':  # 如果URL的协议是HTTP，则将其转换为HTTPS
                    location = parsed_location.scheme + 's' + '://' + parsed_location.netloc + parsed_location.path
                    response = session.get(location, headers={"User-Agent": ua}, cookies=cookie, data=post,
                                           timeout=timeout / 1000, allow_redirects=True)
            return response
        except requests.exceptions.RequestException as error:
            response = error
            error_log(error)
        return response
    else:
        print("请检查网络")
        return 0


def web_request_plus(url, headers, cookie=None, post=None, timeout=5000):
    headers['User-Agent'] = ua
    if check_network():
        url = check_protocol(url)
        try:
            disable_warnings()
            session = requests.Session()
            session.verify = False  # 关闭SSL校验
            response = session.get(url, headers=headers, cookies=cookie, data=post,
                                   timeout=timeout / 1000,
                                   allow_redirects=True)
            if response.is_redirect:  # 检查是否发生重定向
                location = response.headers['Location']
                parsed_location = parse_url(location)
                if parsed_location.scheme == 'http':  # 如果URL的协议是HTTP，则将其转换为HTTPS
                    location = parsed_location.scheme + 's' + '://' + parsed_location.netloc + parsed_location.path
                    response = session.get(location, headers=headers, cookies=cookie, data=post,
                                           timeout=timeout / 1000, allow_redirects=True)
            return response
        except requests.exceptions.RequestException as error:
            response = error
            error_log(error)
        return response
    else:
        print("请检查网络")
        return 0


def raw_request(url, payload):
    parsed_url = urlparse(url)
    if url.startswith("https://"):
        https_flag = True
        host = parsed_url.netloc
        port = parsed_url.port
        if port is None:
            port = 443
    elif url.startswith("http://"):
        https_flag = False
        host = parsed_url.netloc
        port = parsed_url.port
        if port is None:
            port = 80
    else:
        return 0
    ip_address = socket.gethostbyname(host)

    payload = payload.format(host, port).encode()
    print(payload)

    # 创建socket对象
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client_socket.setblocking(False)
    if https_flag:
        # 使用ssl模块创建ssl上下文
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        ssl_context.options |= ssl.OP_NO_SSLv2
        ssl_context.options |= ssl.OP_NO_SSLv3
        ssl_context.verify_mode = ssl.CERT_NONE
        ssl_socket = ssl_context.wrap_socket(client_socket, server_hostname=url)
        # 连接到目标服务器
        ssl_socket.connect((ip_address, port))
        ssl_socket.sendall(payload)
        # response_data = ssl_socket.recv(10000)
        response_data = b''
        while len(response_data) < 10500:
            packet = ssl_socket.recv(1024)
            # time.sleep(1)
            if not packet:
                # break
                exit()
            response_data += packet
        ssl_socket.close()
        return response_data
    else:
        # 创建socket对象
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 连接到目标服务器
        client_socket.connect((ip_address, port))
        # 发送HTTP请求消息
        client_socket.sendall(payload)
        # 接收并打印服务器的响应
        response_data = client_socket.recv(10000)
        # 关闭连接
        client_socket.close()
        return response_data
