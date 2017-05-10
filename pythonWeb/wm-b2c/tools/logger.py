# -*- coding:utf-8 -*-

"""
@author: delu
@file: logger.py
@time: 17/4/25 下午4:34
"""

# import logging
# from logging.handlers import RotatingFileHandler
# from logging.handlers import TimedRotatingFileHandler
#
# pylogger = logging
# pylogger.basicConfig(level=logging.DEBUG,
#                      format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                      datefmt='%Y-%m-%d %H:%M:%S',
#                      filename='/opt/logs/py.log',
#                      filemode='a')
# # 定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
# console = logging.StreamHandler()
# console.setLevel(logging.INFO)
# formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# console.setFormatter(formatter)
# pylogger.getLogger('').addHandler(console)
#
# # 定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
# Rthandler = RotatingFileHandler('/opt/logs/py-info.log', maxBytes=10 * 1204 * 1204, backupCount=5)
# Rthandler.setLevel(logging.INFO)
# formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# Rthandler.setFormatter(formatter)
# pylogger.getLogger('').addHandler(Rthandler)
#
# # 创建TimedRotatingFileHandler对象
# log_file_handler = TimedRotatingFileHandler(filename="/opt/logs/localhost", when="D", interval=1, backupCount=100)
# log_file_handler.setLevel(logging.INFO)
# formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# Rthandler.setFormatter(formatter)
# pylogger.getLogger('').addHandler(Rthandler)
#
# for i in range(10):
#     pylogger.info('hello')
