# -*- coding:utf-8 -*-

"""
@author: delu
@file: gunicorn.py.py
@time: 18/9/1 12:23
"""
# import gevent.monkey
# gevent.monkey.patch_all()
import multiprocessing
bind = '0.0.0.0:9000'      #绑定ip和端口号
backlog = 512                #监听队列
timeout = 30      #超时
worker_class = 'tornado' #使用gevent模式，还可以使用sync 模式，默认的是sync模式
pidfile = '/apps/web/logs/gunicorn.pid'
workers = multiprocessing.cpu_count() * 2 + 1    #进程数
threads = 2 #指定每个进程开启的线程数
loglevel = 'info' #日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
accesslog = "/apps/web/logs/gunicorn_access.log"      #访问日志文件
errorlog = "/apps/web/logs/gunicorn_error.log"        #错误日志文件