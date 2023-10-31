"""  
@Time: 2023/10/27 21:51 
@Auth: Y5neKO
@File: Weblogic.py 
@IDE: PyCharm

Weblogic指纹
"""
import sys

from core import request
from core.color import color


def run(url, timeout):
    response = request.web_request(url, timeout=timeout)
    if 'Hypertext Transfer Protocol' in response.text:
        return 1, "[" + color("+", "green") + "]目标[ {} ]存在[".format(url) + color("Weblogic", "orange") + "]漏洞"
    else:
        return 0, "[" + color("-", "red") + "]目标[ {} ]不存在[Weblogic]漏洞".format(url)


if __name__ == '__main__':
    url = sys.argv[1]
    timeout = sys.argv[2]
    run(url, timeout)
