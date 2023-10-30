"""
@Time: 2023/10/26 20:45
@Auth: Y5neKO
@File: console.py
@IDE: PyCharm

主控制台系统
"""

import argparse
import json
from bs4 import BeautifulSoup

from core.color import *
from core.request import *
from core.log import *
from poc.index import *


def web_info(url):
    parsed_url = urlparse(url)
    response = requests.get(url, timeout=3)
    protocal = parsed_url.scheme
    host = parsed_url.netloc
    port = parsed_url.port
    uri = parsed_url.path
    if port is None:
        port = 80
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string
    print("[*]--------------------目标信息--------------------")
    print("Title: " + title)
    print("Prot:  " + protocal)
    print("Host:  " + host)
    print("Port:  " + str(port))
    print("Uri:   " + uri)


def identify(url, timeout):
    print("回显窗口:\n")
    web_info(url)
    print("[*]--------------------任务开始--------------------")
    finger_base(url, timeout)
    print("[*]--------------------任务结束--------------------")


def scan(url, timeout):
    print("回显窗口:\n")
    print("[*]--------------------任务开始--------------------")
    ez_poc_base(url, timeout=timeout)
    for i in poc_index:
        res = poc_base(i, url, timeout)
        if res[0]:
            normal_log(res[1])
        print(res[1])
    print("[*]--------------------任务结束--------------------")


def exp(url, timeout):
    print("回显窗口:\n")
    print("[*]--------------------任务开始--------------------")
    print("exp模块")
    print("[*]--------------------任务结束--------------------")


def finger_base(url, timeout):
    with open("./finger/finger.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)
        for asset_name, info in json_data['AssetName'].items():
            # print(f'Asset Name: {asset_name}')
            # print(f'Description: {info["description"]}')
            # print(f'Payload Method: {info["payload"]["method"]}')
            # print(f'Payload URI: {info["payload"]["uri"]}')
            # print(f'Payload Headers: {info["payload"]["headers"]}')
            # print(f'Payload Body: {info["payload"]["body"]}')
            # print(f'Keywords: {info["keywords"]}')
            # print('---')

            response = web_request_plus(url, headers=info["payload"]["headers"], post=info["payload"]["body"], timeout=timeout)
            if re.search(info["keywords"], response.text) or re.search(info["keywords"], str(response.headers)):
                # print(response.text)
                result = ("[" + color("+", "green") + "]目标 " + url + " 存在" + color(asset_name, "orange") + "特征")
                print(result)
                normal_log(result)
            else:
                # print(response.text)
                result = ("[" + color("-", "red") + "]目标 " + url + " 不存在" + asset_name + "特征")
                print(result)


def poc_base(poc_name, url, timeout):
    try:
        url = check_protocol(url)
        flag, res = eval(poc_name).run(url, timeout)
        return flag, res
    except Exception as error:
        error_log(str(error))
        pass


def ez_poc_base(url, timeout):
    with open("./ez_poc/ez_poc.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)
        for poc_name, info in json_data['PocName'].items():
            response = web_request_plus(url, headers=info["payload"]["headers"], post=info["payload"]["body"],
                                        timeout=timeout)
            if re.search(info["keywords"], response.text) or re.search(info["keywords"], str(response.headers)):
                # print(response.text)
                result = ("[" + color("+", "green") + "]目标 " + url + " 存在" + color(poc_name, "orange") + "漏洞")
                print(result)
                normal_log(result)
            else:
                # print(response.text)
                result = ("[" + color("-", "red") + "]目标 " + url + " 不存在" + poc_name + "漏洞")
                print(result)


def exp_base():
    print("exp基础利用模块")


def main():
    # 扫描参数
    parser = argparse.ArgumentParser(description="使用帮助")
    scanner = parser.add_argument_group('扫描参数')
    scanner.add_argument("-u", type=str, dest="url", help="目标url, example: http(s)://www.baidu.com/")
    scanner.add_argument("-e", type=str, dest="extension", default="identify", choices=["identify", "scan", "exp"],
                         help="指定操作类型, 默认为资产识别。identify:资产识别 | scan:漏洞扫描 | exp:漏洞利用")
    scanner.add_argument("--scan", type=str, dest="scan", choices=["All", "Shiro", "Weblogic"],
                         help="基础扫描, 使用poc目录内插件:Shiro,Weblogic, 不指定默认全部扫描")
    scanner.add_argument("-t", type=int, dest="timeout", default=5000, help="设置超时时间(ms), 默认5000ms")
    scanner.add_argument("--proxy", type=str, dest="proxy", help="使用代理, 目前仅支持Socks")
    scanner.add_argument("-o", type=str, dest="output", help="输出扫描结果到指定路径")

    scanner2 = parser.add_argument_group('拓展参数')
    scanner2.add_argument('--add-exp', type=str, dest="add_exp_name", help="添加exp插件")

    args = parser.parse_args()

    if args.url and args.extension == "identify":
        try:
            identify(args.url, timeout=args.timeout)
        except ConnectionError as error:
            error_log("core.console->main()->identify模块|" + str(error))
            print("[*]--------------------连接错误--------------------")

    elif args.url and args.extension == "scan":
        try:
            scan(args.url, timeout=args.timeout)
        except ConnectionError as error:
            error_log("core.console->main()->scan模块|" + str(error))
            print("[*]--------------------连接错误--------------------")

    elif args.url and args.extension == "exp":
        try:
            exp(args.url, timeout=args.timeout)
        except ConnectionError as error:
            error_log("core.console->main()->exp模块|" + str(error))
            print("[*]--------------------连接错误--------------------")
