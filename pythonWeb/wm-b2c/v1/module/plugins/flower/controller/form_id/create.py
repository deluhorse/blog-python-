# -*- coding:utf-8 -*-

"""
@author: delu
@file: create.py
@time: 17/5/2 下午2:26
"""
from base.base import Base


class Controller(Base):

    auth = (('buyer',), 'post')

    def initialize(self):
        Base.initialize(self)

    def index(self):
        params = {
            'form_id': self.params('form_id'),
            'goods_id': self.params('goods_id'),
            'buyer_id': self.buyer_user_data['buyer_id']
        }
        # self.do_service(service_path, method_name, params)
        res = self.do_service('plugins.flower.service.mini_app_service', 'create_form_id', params=params)
        self.out(res)
