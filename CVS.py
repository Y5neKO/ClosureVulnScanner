#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Time: 2023/10/26 20:45
@Auth: Y5neKO
@File: CVS.py
@IDE: PyCharm

主程序入口
"""
import signal

from core.banner import banner
from core.console import *


def signal_handler(sig, frame):
    print('收到 Ctrl+C，停止程序...')
    sys.exit(0)


def run():
    print(banner)
    print("欢迎使用Closure Vulnerability Scanner")
    print("Github: https://github.com/Y5neKO\n")
    main()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    run()
