"""  
@Time: 2023/10/27 17:30 
@Auth: Y5neKO
@File: proxy.py 
@IDE: PyCharm

代理系统
"""
import re
import socks
import socket

from core.log import error_log


def proxy(proxy_addr):
    """
    代理模块
    @param proxy_addr: 代理完整地址
    @return: Flag
    """
    match = re.search(r"//(\d+\.\d+\.\d+\.\d+):(\d+)", proxy_addr)
    if match:
        # 提取IP地址和端口号
        ip_address = match.group(1)
        port_number = match.group(2)
        if proxy_addr.startswith("socks://"):
            socks.set_default_proxy(socks.SOCKS5, ip_address, int(port_number))
        elif proxy_addr.startswith("http://"):
            socks.set_default_proxy(socks.HTTP, ip_address, int(port_number))
        socket.socket = socks.socksocket
        return 1
    else:
        print("代理格式错误")
        error_log("代理格式错误")
        return 0
