# -*- coding:utf-8 -*-

"""
@author: delu
@file: send.py
@time: 17/5/5 下午2:15
"""
from base.base import Base


class Controller(Base):
    auth = (('seller',), 'post')

    def initialize(self):
        Base.initialize(self)

    def index(self):
        params = {
            'order_id': self.params('order_id'),
            'logiscomp_id': self.params('logiscomp_id'),
            'tracking_id': self.params('tracking_id'),
            'remark': self.params('remark'),
            'shop_id': self.user_data['shop_id']
        }
        # self.do_service(service_path, method_name, params)
        res = self.do_service('order.service.order_send_service', 'create_send', params=params)
        self.out(res)
