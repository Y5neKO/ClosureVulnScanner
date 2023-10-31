"""  
@Time: 2023/10/26 20:53 
@Auth: Y5neKO
@File: Shiro550.py
@IDE: PyCharm

Shiro框架指纹
"""
import sys

from core import request
from core.color import color


def run(url, timeout):
    response = request.web_request(url, {"rememberMe": "123"}, timeout=timeout)
    try:
        set_cookie = response.headers['set-Cookie']
        if 'rememberMe=deleteMe' in set_cookie:
            return 1, "[" + color("+", "green") + "]目标[ {} ]存在[".format(url) + color("Shiro框架", "orange") + "]漏洞"
        else:
            return 0, "[" + color("-", "red") + "]目标[ {} ]不存在[Shiro框架]漏洞".format(url)
    except:
        return 0, "[" + color("-", "red") + "]目标[ {} ]不存在[Shiro框架]漏洞".format(url)


if __name__ == '__main__':
    url = sys.argv[1]
    timeout = sys.argv[2]
    run(url, timeout)
