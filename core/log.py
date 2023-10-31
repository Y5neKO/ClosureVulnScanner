"""
@Time: 2023/10/26 20:45
@Auth: Y5neKO
@File: log.py
@IDE: PyCharm

日志系统
"""

import datetime
import logging
import os
import re

now = datetime.datetime.now()
formatted_date = now.strftime("%Y-%m-%d")
if not os.path.exists('./log'):
    os.makedirs('./log')


def normal_log(log):
    log = re.sub('\033\[\d+m', '', log)
    logger = logging.getLogger()
    fh = logging.FileHandler(filename='./log/normal_log_' + formatted_date + '.log', encoding="utf-8", mode="a")
    formatter = logging.Formatter('%(asctime)s %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.setLevel(logging.INFO)
    logger.info(log)


def error_log(log):
    log = re.sub('\033\[\d+m', '', log)
    logger = logging.getLogger()
    fh = logging.FileHandler(filename='./log/error_log_' + formatted_date + '.log', encoding="utf-8", mode="a")
    formatter = logging.Formatter('%(asctime)s %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.setLevel(logging.INFO)
    logger.info(log)