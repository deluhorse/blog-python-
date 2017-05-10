# -*- coding:utf-8 -*-

"""
@author: delu
@file: query.py
@time: 17/4/27 上午9:06
"""
from base.base import Base


class Controller(Base):

    auth = (('buyer', 'seller'), 'get')

    def initialize(self):
        Base.initialize(self)

    def index(self):
        params = {
            'start_time': self.params('start_time'),
            'end_time': self.params('end_time'),
            'page_index': self.params('page_index') if self.params('page_index') else '0',
            'page_size': self.params('page_size') if self.params('page_size') else '100'
        }

        if self.user_data and 'shop_id' in self.user_data:
            params['shop_id'] = self.user_data['shop_id']
        if self.buyer_user_data:
            params['buyer_id'] = self.buyer_user_data['buyer_id']

        # self.do_service(service_path, method_name, params)
        res = self.do_service('order.service.order_query_service', 'query_order', params=params)

        self.out(res)
