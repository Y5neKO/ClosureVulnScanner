"""
@Time: 2023/10/26 20:45
@Auth: Y5neKO
@File: banner.py
@IDE: PyCharm
"""

from core import request
from core.color import *

version = "0.0"
# 调用一言接口
if request.check_network():
    hitokoto = request.web_request("https://v1.jinrishici.com/rensheng.txt").text
else:
    hitokoto = "Closure Vulnerability Scanner"

banner = """
    ,ad8888ba,   88                                                   
   d8"'    `"8b  88                                                   
  d8'            88                                                   
  88             88   ,adPPYba,   ,adPPYba,  88       88  8b,dPPYba,   ,adPPYba,
  88             88  a8"     "8a  I8[    ""  88       88  88P'   "Y8  a8P_____88
  Y8,            88  8b       d8   `"Y8ba,   88       88  88          8PP"""""""
   Y8a.    .a8P  88  "8a,   ,a8"  aa    ]8I  "8a,   ,a88  88          "8b,   ,aa
    `"Y8888Y"'   88   `"YbbdP"'   `"YbbdP"'   `"YbbdP'Y8  88           `"Ybbd8"'
    
                                                                           v{} By {} :)
                                                                           {}
""".format(color(version, "cyan"), color("Y5neKO", "yellow"), hitokoto)

banner2 = """
"""
