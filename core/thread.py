"""  
@Time: 2024/2/27 15:12 
@Auth: Y5neKO
@File: thread.py
@IDE: PyCharm 
"""
import threading
import time
import hashlib

from core.color import *
from core.request import *
from poc.index import *


"""
线程锁，防止竞争输出导致输出到文件乱码
"""
lock = threading.Lock()
"""
扫描结果集
"""
result_list = []


def calculate_url_hash(url, hash_method='md5'):
    """
    Retrieves the content from the provided URL and calculates its hash.

    :param url: The URL of the content to hash
    :param hash_method: The hashing method to use (default is 'sha256')
    :return: The hex digest of the hash
    """
    # Choose the hashing algorithm
    hash_function = getattr(hashlib, hash_method)()

    # Retrieve the content from the URL
    response = requests.get(url)

    # Check for a successful request
    if response.status_code == 200:
        # Update the hash with the content of the URL
        hash_function.update(response.content)
        # Return the hex digest of the hash
        return hash_function.hexdigest()
    elif re.search(r'404|NOT FOUND', response.text):
        # raise Exception(f"Content not found at URL: {url}")
        return "404"
    else:
        # raise Exception(f"Failed to retrieve content from URL: {url}")
        return "无法连接"


class ThreadPool:
    def __init__(self, max_threads):
        self.max_threads = max_threads
        self.lock = threading.Lock()
        self.threads = set()

    def worker(self, thread_id):
        with self.lock:
            print(f"Thread {thread_id} started")
            # Your thread's work goes here
            time.sleep(2)
            print(f"Thread {thread_id} finished")
            self.threads.remove(threading.current_thread())

    def submit(self):
        with self.lock:
            if len(self.threads) < self.max_threads:
                thread_id = len(self.threads)
                thread = threading.Thread(target=self.worker, args=(thread_id,))
                self.threads.add(thread)
                thread.start()


# 指纹识别相关
def finger_base(url, timeout, asset_name, info):
    """
    指纹基础模块，用于指纹识别模块调用
    @param url: 链接
    @param timeout: 超时时间
    @param asset_name: 资产名称
    @param info: 指纹详细信息
    @return: Flag
    """
    response = web_request_plus(url.rstrip() + info["payload"]['uri'], headers=info["payload"]["headers"],
                                post=info["payload"]["body"], timeout=timeout)
    flag = 0  # 验证标识
    if info['location'] == "uri":
        if response.status_code == 200:
            flag = 1
        if re.search(r'404|NOT FOUND', response.text):
            flag = 0  # 某些网站404状态码不返回在响应头中
    elif info['location'] == "headers":
        if re.search(re.compile(info['keywords']), str(response.headers)):
            flag = 1
    elif info['location'] == "body":
        if re.search(re.compile(info['keywords']), str(response.text)):
            flag = 1
    if info['checkhash'] != "":
        if calculate_url_hash(url.rstrip() + info["payload"]['uri']) != info['checkhash']:
            flag = 0
    # 输出结果
    if flag:
        result = ("[" + color("+", "green") + "]目标[ " + url + " ]存在[" + color(asset_name, "orange") + "]特征")
        result_list.append("[" + color("+", "green") + "]目标[ " + url + " ]存在[" + color(asset_name, "orange") + "]特征")
        normal_log(result)
    else:
        result = ("[" + color("-", "red") + "]目标[ " + url + " ]不存在[" + asset_name + "]特征")
    with lock:
        print(result)
    return 1


# 漏洞扫描相关
def ez_poc_base(url, timeout, poc_name, info):
    """
    简单poc验证模块，用于漏洞扫描模块调用(复用自finger_base模块，功能类似)
    @param url:
    @param timeout:
    @param poc_name:
    @param info:
    @return:
    """
    response = web_request_plus(url.rstrip() + info["payload"]['uri'], headers=info["payload"]["headers"],
                                post=info["payload"]["body"], timeout=timeout)
    flag = 0  # 验证标识
    if info['location'] == "uri":
        if response.status_code == 200:
            flag = 1
        if re.search(r'404|NOT FOUND', response.text):
            flag = 0  # 某些网站404状态码不返回在响应头中
    elif info['location'] == "headers":
        if re.search(re.compile(info['keywords']), str(response.headers)):
            flag = 1
    elif info['location'] == "body":
        if re.search(re.compile(info['keywords']), str(response.text)):
            flag = 1
    # 输出结果
    if flag:
        result = ("[" + color("+", "green") + "]目标[ " + url + " ]存在[" + color(poc_name, "orange") + "]漏洞")
        result_list.append(
            "[" + color("+", "green") + "]目标[ " + url + " ]存在[" + color(poc_name, "orange") + "]漏洞\npayload为: \n" + "url: " + response.url + "\n" + "data: " + str(info['payload']))
        normal_log(result)
    else:
        result = ("[" + color("-", "red") + "]目标[ " + url + " ]不存在[" + poc_name + "]漏洞")
    with lock:
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
        result_list.append(
            "[" + color("+", "green") + "]目标[ " + url + " ]存在[" + color(res['name'], "orange") + "]漏洞, payload: \n" + "url: " + res['url'] + "\n" + "data: " + str(res['payload']))
    else:
        result = ("[" + color("-", "red") + "]目标[ " + url + " ]不存在[" + res['name'] + "]漏洞")
    with lock:
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
        print(error)
        pass
