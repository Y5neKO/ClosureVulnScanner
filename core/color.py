"""  
@Time: 2023/10/27 17:37 
@Auth: Y5neKO
@File: color.py
@IDE: PyCharm

色彩输出系统
"""
# 黑色
BLACK = '\033[30m'
# 红色
RED = '\033[31m'
# 绿色
GREEN = '\033[32m'
# 黄色
YELLOW = '\033[33m'
# 蓝色
BLUE = '\033[34m'
# 紫色
PURPLE = '\033[35m'
# 青色
CYAN = '\033[36m'
# 白色
WHITE = '\033[37m'
# 橙色
ORANGE = '\033[93m'
# 默认颜色
DEFAULT = '\033[39m'
# 重置序列
CLEAR = '\033[0m'


def color(str, color) -> str:
    return {
        "red": RED + str + CLEAR,
        "black": BLACK + str + CLEAR,
        "green": GREEN + str + CLEAR,
        "yellow": YELLOW + str + CLEAR,
        "blue": BLUE + str + CLEAR,
        "purple": PURPLE + str + CLEAR,
        "cyan": CYAN + str + CLEAR,
        "white": WHITE + str + CLEAR,
        "orange": ORANGE + str + CLEAR
    }.get(color, WHITE + str + CLEAR)
