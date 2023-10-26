"""
@Time: 2023/10/26 20:45
@Auth: Y5neKO
@File: log.py
@IDE: PyCharm
"""

import datetime
import logging
import os

now = datetime.datetime.now()
formatted_date = now.strftime("%Y-%m-%d")
if not os.path.exists('./log'):
    os.makedirs('./log')

logging.basicConfig(filename='./log/log_' + formatted_date + '.log',
                    format='%(asctime)s %(message)s',
                    filemode="a", level=logging.INFO)


def normal_log(log):
    logging.info(log)
