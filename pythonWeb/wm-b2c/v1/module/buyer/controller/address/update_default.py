# -*- coding:utf-8 -*-

"""
@author: delu
@file: update_default.py
@time: 17/4/27 下午4:41
"""
from base.base import Base


class Controller(Base):

    auth = (('buyer',), 'post')

    def initialize(self):
        Base.initialize(self)

    def index(self):
        params = {
            'buyer_id': self.buyer_user_data['buyer_id'],
            'addr_no': self.params('addr_no')
        }
        # self.do_service(service_path, method_name, params)
        res = self.do_service('buyer.service.address.buyer_address_service', 'update_default_addr', params=params)

        self.out(res)
