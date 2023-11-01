"""
@Time: 2023/10/26 20:45
@Auth: Y5neKO
@File: console.py
@IDE: PyCharm

主控制台系统
"""

import argparse
import json
import sys
import threading

import socks
from bs4 import BeautifulSoup

from core.color import *
from core.log import *
from core.request import *
from poc.index import *
from exp.index import *


def web_info(url):
    """
    头部输出目标主要信息
    @param url: 地址
    @return: Flag
    """
    parsed_url = urlparse(url)
    response = requests.post(url, timeout=3)
    response.encoding = "utf-8"
    protocal = parsed_url.scheme
    host = parsed_url.netloc
    port = parsed_url.port
    uri = parsed_url.path
    if port is None:
        port = 80
        if protocal == "https":
            port = 443
    soup = BeautifulSoup(response.text, "html.parser")
    try:
        title = soup.title.string
    except:
        title = "无"
    print("[*]--------------------目标信息--------------------")
    print("Title: " + title)
    print("Proto: " + protocal)
    print("Host:  " + host)
    print("Port:  " + str(port))
    print("Uri:   " + uri)
    if socks.get_default_proxy():
        print("Proxy: " + color("On", "green"))
    else:
        print("Proxy: " + color("Off", "red"))
    return 1


def identify(url, timeout):
    """
    资产识别模块
    @param url: 地址
    @param timeout: 超时时间
    @return: Flag
    """
    threads = []
    print("回显窗口:\n")
    web_info(url)
    print("[*]--------------------任务开始--------------------")
    with open("./finger/finger.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)
        # 多线程操作
        for asset_name, info in json_data['AssetName'].items():
            t = threading.Thread(target=finger_base, args=(url, timeout, asset_name, info))
            threads.append(t)
            t.start()
    for t in threads:
        t.join()
    print("[*]--------------------任务结束--------------------")
    return 1


def scan(url, timeout):
    """
    漏洞扫描模块
    @param url: 地址
    @param timeout: 超时时间
    @return: Flag
    """
    threads = []
    threads2 = []
    print("回显窗口:\n")
    web_info(url)
    print("[*]--------------------任务开始--------------------")
    # 首先进行简单poc验证
    with open("./ez_poc/ez_poc.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)
        # 多线程操作
        for asset_name, info in json_data['PocName'].items():
            t = threading.Thread(target=ez_poc_base, args=(url, timeout, asset_name, info))
            threads.append(t)
            t.start()
    for t in threads:
        t.join()

    # 接着在进行复杂poc验证
    # 多线程操作
    for i in poc_index:
        t2 = threading.Thread(target=poc_thread_func, args=(i, url, timeout))   # 通过poc_thread_func方法进行多线程操作
        threads2.append(t2)
        t2.start()
    for t2 in threads2:
        t2.join()
    print("[*]--------------------任务结束--------------------")
    return 1


def exp(url, exp_name, cmd, timeout):
    """
    exp利用模块
    @param cmd: 命令
    @param exp_name: exp名称
    @param url: 地址
    @param timeout: 超时时间
    @return: Flag
    """
    print("回显窗口:\n")
    web_info(url)
    print("[*]--------------------任务开始--------------------")
    flag, res = exp_base(url, exp_name, cmd, timeout)
    res = extract_cmd(res)
    print("命令执行结果:")
    print(res)
    print("[*]--------------------任务结束--------------------")
    return 1


def finger_base(url, timeout, asset_name, info):
    """
    指纹基础模块，用于资产识别模块调用
    @param url: 链接
    @param timeout: 超时时间
    @param asset_name: 资产名称
    @param info: 指纹详细信息
    @return: Flag
    """
    response = web_request_plus(url, headers=info["payload"]["headers"], post=info["payload"]["body"], timeout=timeout)
    if re.search(info["keywords"], response.text) or re.search(info["keywords"], str(response.headers)):
        result = ("[" + color("+", "green") + "]目标[ " + url + " ]存在[" + color(asset_name, "orange") + "]特征")
        print(result)
        normal_log(result)
    else:
        result = ("[" + color("-", "red") + "]目标[ " + url + " ]不存在[" + asset_name + "]特征")
        print(result)
    return 1


def poc_thread_func(i, url, timeout):
    """
    复杂poc验证多线程模块，用于漏洞扫描模块调用
    @param i: 线程索引
    @param url: 地址
    @param timeout: 超时时间
    @return: Flag
    """
    res = poc_base(i, url, timeout)
    if res['vulnerable']:
        result = ("[" + color("+", "green") + "]目标[ " + url + " ]存在[" + color(res['name'], "orange") + "]漏洞")
        normal_log(result)
    else:
        result = ("[" + color("-", "red") + "]目标[ " + url + " ]不存在[" + res['name'] + "]漏洞")
    print(result)


def poc_base(poc_name, url, timeout):
    """
    复杂poc验证基础模块，用于漏洞扫描模块调用
    @param poc_name: poc目录内的poc索引名称
    @param url: 地址
    @param timeout: 超时时间
    @return: 验证结果
    """
    try:
        res = eval(poc_name).run(url, timeout)
        return res
    except Exception as error:
        pass


def ez_poc_base(url, timeout, poc_name, info):
    """
    简单poc验证模块，用于漏洞扫描模块调用
    @param url:
    @param timeout:
    @param poc_name:
    @param info:
    @return:
    """
    response = web_request_plus(url, headers=info["payload"]["headers"], post=info["payload"]["body"], timeout=timeout)
    if re.search(info["keywords"], response.text) or re.search(info["keywords"], str(response.headers)):
        result = ("[" + color("+", "green") + "]目标[ " + url + " ]存在[" + color(poc_name, "orange") + "]漏洞")
        print(result)
        normal_log(result)
    else:
        result = ("[" + color("-", "red") + "]目标[ " + url + " ]不存在[" + poc_name + "]漏洞")
        print(result)


def exp_base(url, exp_name, cmd, timeout):
    try:
        flag, res = eval(exp_name).run(url, cmd)
        return flag, res
    except Exception as error:
        pass


def extract_cmd(input_string):
    """
    提取命令执行结果，标识：{{{{{cmd_result}}}}}
    @param input_string:
    @return:
    """
    pattern = r'\{\{\{\{\{([^{}]*)\}\}\}\}\}'
    matches = re.search(pattern, input_string)
    if matches:
        return matches.group(1)


def proxy(proxy_addr):
    """
    代理模块
    @param proxy_addr: 代理完整地址
    @return: Flag
    """
    match = re.search(r"//(\d+\.\d+\.\d+\.\d+):(\d+)", proxy_addr)
    if match:
        # 提取IP地址和端口号
        ip_address = match.group(1)
        port_number = match.group(2)
        if proxy_addr.startswith("socks://"):
            socks.set_default_proxy(socks.SOCKS5, ip_address, int(port_number))
        elif proxy_addr.startswith("http://"):
            socks.set_default_proxy(socks.HTTP, ip_address, int(port_number))
        socket.socket = socks.socksocket
        return 1
    else:
        print("代理格式错误")
        error_log("代理格式错误")
        return 0


class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding="utf-8")  # 防止编码错误

    def write(self, message):
        self.terminal.write(message)
        message = re.sub(r'\033\[\d+m', '', message)
        self.log.write(message)

    def flush(self):
        pass


def main():
    """
    控制台主入口
    @return: Flag
    """
    parser = argparse.ArgumentParser(description="使用帮助")
    scanner = parser.add_argument_group('扫描参数')
    scanner.add_argument("-u", type=str, dest="url", help="目标url, example: http(s)://www.baidu.com/")
    scanner.add_argument("-e", type=str, dest="extension", default="identify", choices=["identify", "scan", "exp"],
                         help="指定操作类型, 默认为资产识别。identify:资产识别 | scan:漏洞扫描 | exp:漏洞利用")
    # scanner.add_argument("--scan", type=str, dest="scan", default="all",
    #                     help="基础扫描, 使用poc目录内插件:Shiro,Weblogic, 不指定默认全部扫描")
    scanner.add_argument("--exp", type=str, dest="exp_name", help="指定exp模块, 使用exp目录内插件")
    scanner.add_argument("--cmd", type=str, dest="cmd", default="whoami", help="指定exp模块执行的命令, 若模块不支持命令执行可缺省")
    scanner.add_argument("-t", type=int, dest="timeout", default=5000, help="设置超时时间(ms), 默认5000ms")
    scanner.add_argument("--proxy", type=str, dest="proxy",
                         help="使用代理, 目前支持Socks,HTTP; 格式:{socks|http}://ip_addr:port")
    scanner.add_argument("-o", type=str, dest="output", help="输出扫描结果到指定路径")

    scanner2 = parser.add_argument_group('拓展参数')
    scanner2.add_argument('--list', type=str, dest="list_name", choices=["poc", "exp"], help="列出已经加载的poc/exp插件")
    scanner2.add_argument('--add-poc', type=str, dest="add_poc_name", help="添加poc插件")
    scanner2.add_argument('--add-exp', type=str, dest="add_exp_name", help="添加exp插件")

    args = parser.parse_args()

    if args.output:
        log = Logger(args.output)
        sys.stdout = log

    if args.proxy:  # 设置全局代理
        proxy(args.proxy)

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
        if args.exp_name and args.cmd:
            try:
                exp(args.url, args.exp_name + "_exp", args.cmd, timeout=args.timeout)
            except ConnectionError as error:
                error_log("core.console->main()->exp模块|" + str(error))
                print("[*]--------------------连接错误--------------------")
        else:
            print("EXP模块未指定名称")

    elif args.list_name == "poc":
        print("已经加载的poc插件:")
        for i in poc_index:
            i = i.replace("_poc", "")
            print(i)

    elif args.list_name == "exp":
        print("已经加载的exp插件:")
        for i in exp_index:
            i = i.replace("_exp", "")
            print(i)

    elif args.add_poc_name:
        with open('./poc/index.py', 'r', encoding="utf-8") as file:
            # 读取文件内容
            content = file.read()
        new_content = content.replace(']', ', "' + args.add_poc_name + '_poc"]')
        new_content = new_content.replace('\n\npoc_index',
                                          '\nfrom poc import ' + args.add_poc_name + ' as ' + args.add_poc_name + '_poc\n\npoc_index')
        # print(new_content)
        with open('./poc/index.py', 'w', encoding="utf-8") as file:
            file.write(new_content)
        print("[{}]模块添加成功".format(args.add_poc_name))

    elif args.add_exp_name:
        with open('./exp/index.py', 'r', encoding="utf-8") as file:
            # 读取文件内容
            content = file.read()
        new_content = content.replace(']', ', "' + args.add_exp_name + '_exp"]')
        new_content = new_content.replace('\n\nexp_index',
                                          '\nfrom exp import ' + args.add_exp_name + ' as ' + args.add_exp_name + '_exp\n\nexp_index')
        # print(new_content)
        with open('./exp/index.py', 'w', encoding="utf-8") as file:
            file.write(new_content)
        print("[{}]模块添加成功".format(args.add_exp_name))

    return 1
