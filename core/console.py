"""
@Time: 2023/10/26 20:45
@Auth: Y5neKO
@File: console.py
@IDE: PyCharm

主控制台系统
"""

import argparse
from core.request import check_protocol
from finger.index import *
from core.log import *


def identify(url, timeout):
    print("回显窗口:\n")
    print("[*]--------------------任务开始--------------------")
    for i in finger_index:
        res = finger_base(i, url, timeout)
        normal_log(res[1])
        print(res[1])
    print("[*]--------------------任务结束--------------------")


def scan(url, timeout):
    print("回显窗口:\n")
    print("[*]--------------------任务开始--------------------")
    print("scan模块")
    print("[*]--------------------任务结束--------------------")


def finger_base(finger_name, url, timeout):
    try:
        url = check_protocol(url)
        flag, res = eval(finger_name).run(url, timeout)
        return flag, res
    except Exception as error:
        error_log(error)
        pass


def main():
    # 扫描参数
    parser = argparse.ArgumentParser(description="使用帮助")
    scanner = parser.add_argument_group('扫描参数')
    scanner.add_argument("-u", type=str, dest="url", help="目标url, example: http(s)://www.baidu.com/")
    scanner.add_argument("-e", type=str, dest="extension", default="identify", choices=["identify", "scan"],
                         help="指定操作类型, 默认为资产识别。identify:资产识别 | scan:漏洞扫描")
    scanner.add_argument("--scan", type=str, dest="scan", choices=["All", "Shiro", "Weblogic"],
                         help="基础扫描, 使用exp目录内插件:Shiro,Weblogic, 不指定默认全部扫描")
    scanner.add_argument("-t", type=int, dest="timeout", default=5000, help="设置超时时间(ms), 默认5000ms")
    scanner.add_argument("--proxy", type=str, dest="proxy", help="使用代理, 目前仅支持Socks")
    scanner.add_argument("-o", type=str, dest="output", help="输出扫描结果到指定路径")

    scanner2 = parser.add_argument_group('拓展参数')
    # scanner2.add_argument('-aa', )

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
