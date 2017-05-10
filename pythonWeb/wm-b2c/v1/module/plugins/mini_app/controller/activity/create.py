# -*- coding:utf-8 -*-

"""
@author: delu
@file: create.py
@time: 17/5/2 下午4:04
"""
from base.base import Base


class Controller(Base):
    def initialize(self):
        Base.initialize(self)

    def index(self):
        params = {
            'goods_id': self.params('goods_id'),
            'limit_time': int(self.params('limit_time')),
        }
        # self.do_service(service_path, method_name, params)
        res = self.do_service('plugins.mini_app.service.mini_app_service', 'create_activity', params=params)
        self.out(res)
