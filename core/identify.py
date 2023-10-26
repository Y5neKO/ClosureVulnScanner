"""
@Time: 2023/10/26 20:45
@Auth: Y5neKO
@File: identify.py
@IDE: PyCharm
"""

import os
import json


# 遍历目录下所有exp的json
def traverse_folder(folder_path, file_extension=".json"):
    exp_dist = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(file_extension):
                file_path = os.path.join(root, file)
                exp_dist.append(file_path)
                # print(file_path)
    return exp_dist


exp_list = traverse_folder("../finger")
print(exp_list)
