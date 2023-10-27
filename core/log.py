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

now = datetime.datetime.now()
formatted_date = now.strftime("%Y-%m-%d")
if not os.path.exists('./log'):
    os.makedirs('./log')


def normal_log(log):
    logging.basicConfig(filename='./log/normal_log_' + formatted_date + '.log',
                        format='%(asctime)s %(message)s',
                        filemode="a", level=logging.INFO)
    logging.info(log)


def error_log(log):
    logging.basicConfig(filename='./log/error_log_' + formatted_date + '.log',
                        format='%(asctime)s %(message)s',
                        filemode="a", level=logging.DEBUG)
    logging.info(log)
