#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 路由配置
# 增加控制器, 导入控制器文件引用类，并修改route list

import importlib
import os

import config as config

import controller.error as error
import tornado.web

CONF = config.CONF

route = [
    (r"/static/(.*)", tornado.web.StaticFileHandler, dict(path=CONF['static_path'])),
]

"""
初始化项目
"""
version = CONF['version']
host_path = CONF['host_path']
route_path = host_path + version + '/'
root_dir = '../' + version + '/controller'
root_path = 'controller'


def init():
    # 遍历controller文件夹下的所有文件，创建controller实例并放入全局字典中
    look_up_file(root_dir)


# 加载controller
def look_up_file(dir_name):
    for parent, dir_names, file_names in os.walk(dir_name):

        for file_name in file_names:

            if not (file_name.endswith('.pyc') or file_name.startswith('__') or file_name.startswith('base')):
                try:
                    controller_key = root_path + parent.replace(root_dir, '').\
                        replace('/', '.').replace('\\', '.') + '.' + \
                                     file_name.split('.')[0]

                    controller_module = importlib.import_module(controller_key)

                    if hasattr(controller_module, 'Controller'):
                        controller_item = controller_module.Controller

                        route.append(
                            (r"" + route_path + controller_key.replace(root_path + '.', '').
                             replace('.', '/') + '/*', controller_item))

                        print route_path + controller_key.replace(root_path + '.', '').replace('.', '/') + '/*'

                except Exception, e:
                    print Exception, ":", e

        for subdir_name in dir_names:
            look_up_file(subdir_name)


init()

route.append((r".*", error.Error))

setting = config.CONF
