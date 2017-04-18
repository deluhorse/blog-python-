# -*- coding:utf-8 -*-

"""
@author: delu
@file: user_login.py
@time: 17/4/16 上午10:25
"""
from controller.base import Base


class Controller(Base):
    user_service = None

    def initialize(self):
        Base.initialize(self)
        self.user_service = self.import_service('user.user_service')

    def index(self):
        """
        管理员登录
        :return: 
        """
        params = eval(self.params('para'))
        password = params['password']
        acount = params['account']



