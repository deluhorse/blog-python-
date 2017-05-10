# -*- coding:utf-8 -*-

"""
@author: delu
@file: update.py
@time: 17/4/20 下午5:06
更新店铺信息
"""
from base.base import Base


class Controller(Base):

    auth = (('seller',), 'post')

    def initialize(self):
        Base.initialize(self)

    def index(self):
        # self.do_service(service_path, method_name, params)
        res = self.do_service('user.user_service', 'create', params=params)