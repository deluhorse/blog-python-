# -*- coding:utf-8 -*-

"""
@author: delu
@file: user_query.py
@time: 17/4/14 下午4:37
"""
from controller.base import Base


class Controller(Base):
    user_Service = None
    # user_type = ('admin',)

    def initialize(self):
        Base.initialize(self)
        self.user_Service = self.import_service('user.user_service')

    def index(self):
        """
        查询管理员信息
        :return: 
        """
        params = eval(self.params('para'))

        list = self.user_Service.get_user_account(params)

        data = {}

        data['list'] = list

        self.out(0, '成功', data)
