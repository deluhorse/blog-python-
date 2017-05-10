# -*- coding:utf-8 -*-

"""
@author: delu
@file: receive.py
@time: 17/5/5 下午5:24
"""
from base.base import Base


class Controller(Base):
    def initialize(self):
        Base.initialize(self)

    def index(self):
        params = {
            'order_id': self.params('order_id'),
            'buyer_id': self.buyer_user_data['buyer_id']
        }
        # self.do_service(service_path, method_name, params)
        res = self.do_service('order.service.order_send_service', 'create_receive', params=params)