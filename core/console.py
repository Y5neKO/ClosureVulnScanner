"""
@Time: 2023/10/26 20:45
@Auth: Y5neKO
@File: console.py
@IDE: PyCharm
"""

import argparse
from core import request
from exp.index import *


def identify(url):
    print("回显窗口:\n")
    print("[*]--------------------任务开始--------------------")
    respond = request.web_request(url)
    print(respond)
    print("identify")
    print("[*]--------------------任务结束--------------------")


def scan(url):
    print("回显窗口:\n")
    print("[*]--------------------任务开始--------------------")
    for i in exp_index:
        res = exp_base(i, url)
    print("[*]--------------------任务结束--------------------")


def exp_base(exp_name, url):
    try:
        flag, res = eval(exp_name)
        return flag, res
    except:
        pass


def main():
    parser = argparse.ArgumentParser(description="参数")
    scanner = parser.add_argument_group('参数')
    scanner.add_argument("-u", type=str, dest="url", help="目标url, example: http(s)://www.baidu.com/")
    scanner.add_argument("-e", type=str, dest="extension", default="identify", choices=["identify", "scan"],
                         help="指定操作类型, 默认为资产识别。identify:资产识别 | scan:漏洞扫描")
    scanner.add_argument("--scan", type=str, dest="scan", choices=["All", "Shiro", "Weblogic"],
                         help="基础扫描, 使用exp目录内插件:Shiro,Weblogic, 不指定默认全部扫描")
    scanner.add_argument("--proxy", type=str, dest="proxy", help="使用代理, 目前仅支持Socks")
    scanner.add_argument("-o", type=str, dest="output", help="输出扫描结果到指定路径")

    args = parser.parse_args()

    if args.url and args.extension == "identify":
        try:
            identify(args.url)
        except ConnectionError:
            print("[*]--------------------连接错误--------------------")

    elif args.url and args.extension == "scan":
        try:
            scan(args.url)
        except ConnectionError:
            print("[*]--------------------连接错误--------------------")
