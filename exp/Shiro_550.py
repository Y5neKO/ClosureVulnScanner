"""  
@Time: 2023/10/26 20:53 
@Auth: Y5neKO
@File: Shiro_550.py
@IDE: PyCharm 
"""

from core import request


def run(url):
    response = request.web_request(url, "rememberMe=123")
    # response.cookies
