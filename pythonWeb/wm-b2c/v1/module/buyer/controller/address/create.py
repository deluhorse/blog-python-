# -*- coding:utf-8 -*-

"""
@author: delu
@file: create.py
@time: 17/4/27 下午3:27
"""
from base.base import Base


class Controller(Base):

    auth = (('buyer',), 'post')

    def initialize(self):
        Base.initialize(self)

    def index(self):
        params = {
            'city_no': self.params('city_no') if self.params('city_no') else 0,
            'district': self.params('district'),
            'street_addr': self.params('street_addr'),
            'name': self.params('name'),
            'mobile_no': self.params('mobile_no'),
            'scen_type': self.buyer_user_data['scen_type'],
            'scen_id': self.buyer_user_data['scen_id'],
            'buyer_id': self.buyer_user_data['buyer_id']
        }
        redis = self.redis.get_conn()
        params['addr_no'] = redis.incr(self.cache_key_predix.BUYER_ADDR_NO)
        # self.do_service(service_path, method_name, params)
        res = self.do_service('buyer.service.address.buyer_address_service', 'create_buyer_addr', params=params)

        self.out(res, {'addr_no': params['addr_no']})
