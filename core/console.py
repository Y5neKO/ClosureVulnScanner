"""
@Time: 2023/10/26 20:45
@Auth: Y5neKO
@File: console.py
@IDE: PyCharm

主控制台系统
"""

import argparse
import concurrent.futures
import json

from bs4 import BeautifulSoup

from core.proxy import *
from core.thread import *
from exp.index import *
from poc.index import *

"""
默认最大线程数
"""
max_threads = 200


def web_info(url):
    """
    头部输出目标主要信息
    @param url: 地址
    @return: Flag
    """
    parsed_url = urlparse(url)
    try:
        response = requests.post(url, timeout=1)
    except Exception:
        print(color("[ERROR]", "red") + "连接错误，请检查目标地址和连接状态")
        sys.exit(1)
    response.encoding = "utf-8"
    protocal = parsed_url.scheme
    host = parsed_url.netloc
    port = parsed_url.port
    uri = parsed_url.path
    if uri == "":
        uri = "/"
    if port is None:
        port = 80
        if protocal == "https":
            port = 443
    soup = BeautifulSoup(response.text, "html.parser")
    try:
        title = soup.title.string
    except Exception:
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
    指纹识别模块
    @param url: 地址
    @param timeout: 超时时间
    @return: Flag
    """
    print("回显窗口:\n")
    web_info(url)
    print("[*]--------------------任务开始--------------------")
    with open("./finger/finger.json", "r", encoding="utf-8") as file:
        json_data = json.load(file)
        with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
            futures = {executor.submit(finger_base, url, timeout, asset_name, info): (asset_name, info) for
                       asset_name, info in json_data['AssetName'].items()}
            for future in concurrent.futures.as_completed(futures):
                asset_name, info = futures[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"Thread for {asset_name} encountered an error: {e}")
    if len(result_list) > 0:
        print("[*]--------------------扫描结果--------------------")
        for i in range(len(result_list)):
            print(result_list[i])
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
        t2 = threading.Thread(target=poc_thread_func, args=(i, url, timeout))  # 通过poc_thread_func方法进行多线程操作
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


def exp_base(url, exp_name, cmd, timeout):
    try:
        flag, res = eval(exp_name).run(url, cmd)
        return flag, res
    except Exception:
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


def main():
    """
    控制台主入口
    @return: Flag
    """
    parser = argparse.ArgumentParser(description="使用帮助")
    scanner = parser.add_argument_group('扫描参数')
    scanner.add_argument("-u", type=str, dest="url", help="目标url, example: http(s)://www.baidu.com/")
    scanner.add_argument("-e", type=str, dest="extension", default="identify", choices=["identify", "scan", "exp"],
                         help="指定操作类型, 默认为指纹识别。identify:指纹识别 | scan:漏洞扫描 | exp:漏洞利用")
    # scanner.add_argument("--scan", type=str, dest="scan", default="all",
    #                     help="基础扫描, 使用poc目录内插件:Shiro,Weblogic, 不指定默认全部扫描")
    scanner.add_argument("--exp", type=str, dest="exp_name", help="指定exp模块, 使用exp目录内插件")
    scanner.add_argument("--cmd", type=str, dest="cmd", default="whoami",
                         help="指定exp模块执行的命令, 若模块不支持命令执行可缺省")
    scanner.add_argument("-t", type=int, dest="timeout", default=5000, help="设置超时时间(ms), 默认5000ms")
    scanner.add_argument("--proxy", type=str, dest="proxy",
                         help="使用代理, 目前支持Socks,HTTP; 格式:{socks|http}://ip_addr:port")
    scanner.add_argument("-o", type=str, dest="output", help="输出扫描结果到指定路径")

    scanner2 = parser.add_argument_group('拓展参数')
    scanner2.add_argument('--list', type=str, dest="list_name", choices=["poc", "exp"],
                          help="列出已经加载的poc/exp插件")
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
