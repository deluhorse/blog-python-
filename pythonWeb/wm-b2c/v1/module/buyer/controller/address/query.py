# -*- coding:utf-8 -*-

"""
@author: delu
@file: query.py
@time: 17/4/27 下午3:27
"""
from base.base import Base


class Controller(Base):
    auth = (('buyer',), 'get')

    def initialize(self):
        Base.initialize(self)

    def index(self):
        params = {
            'buyer_id': self.buyer_user_data['buyer_id']
        }
        # self.do_service(service_path, method_name, params)
        res = self.do_service('buyer.service.address.buyer_address_service', 'query_address_list', params=params)

        self.out(res)
