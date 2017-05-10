#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 配置文件
CONF = {
    # web服务端口
    'web_port': 8889,
    # 版本
    'version': 'v1',
    'host_path': '/api/',

    # 是否开启调试模式。在调试模式中，修改文件不需要重启服务，且会将错误信息输出到页面
    'debug': True,

    # 数据库
    'isDataBase': True,  # 是否使用数据库，默认为False，开启后，请配置数据库信息

    # redis

    # 静太文件目录
    'static_path': 'static',
    'template_path': 'view',

    # 登录地址 当用户未登录时，系统跳到此地址
    'login_url': '/',

    # 模板设置
    'VIEW_PATH': '../view',

    # WEB title
    'title': 'GameFaqClub',

    # 图片地址
    'PIC': {
        'HOST': '',
        'SUFFIX': ''
    }
}