# -*- coding:utf-8 -*-

"""
@author: delu
@file: query_prepay_id.py
@time: 17/4/26 下午1:56
"""
from base.base import Base


class Controller(Base):
    def initialize(self):
        Base.initialize(self)

    def index(self):
        params = {

        }
        # self.do_service(service_path, method_name, params)
        res = self.do_service('user.user_service', 'create', params=params)