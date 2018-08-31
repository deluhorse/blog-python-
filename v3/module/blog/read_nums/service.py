# -*- coding:utf-8 -*-

"""
@author: delu
@file: service.py
@time: 18/8/31 14:08
"""
from base.service import ServiceBase
import tornado.gen


class Service(ServiceBase):
    """
    service
    """

    user_model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        self.user_model = self.import_model('user.user_model')

    @tornado.gen.coroutine
    def test(self, params={}):
        pass