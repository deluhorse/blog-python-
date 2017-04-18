# -*- coding:utf-8 -*-

"""
@author: delu
@file: user_service.py
@time: 17/4/13 下午3:13
"""
from service.service import ServiceBase


class Service(ServiceBase):
    """
    user_service
    """

    user_model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        self.user_model = self.import_model('user.user_model')

    def create(self, params):
        """
        注册管理员
        :param params: 
        :return: 
        """
        salt = self.salt()
        password = self.md5(self.md5(params['password']) + salt)

        params['password'] = password
        params['salt'] = salt

        res = self.user_model.create(params)

        return res

    def get_user_account(self, params):
        """
        查询管理员
        :param params: 
        :return: 
        """
        list = self.user_model.get_many(params)

        return list

    def login(self, params):
        """
        管理员登录
        :param params: 
        :return: 
        """

