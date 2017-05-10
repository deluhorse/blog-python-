# -*- coding:utf-8 -*-

"""
@author: delu
@file: create.py
@time: 17/4/28 上午9:50
"""
from base.base import Base


class Controller(Base):

    auth = (('buyer',), 'post')

    def initialize(self):
        Base.initialize(self)

    def index(self):
        params = {
            'addr_no': self.params('addr_no'),
            'order_id': self.params('order_id'),
            'receiver_name': self.params('receiver_name'),
            'receiver_mobile': self.params('receiver_mobile'),
            'receiver_address': self.params('receiver_address'),
            'city_no': self.params('city_no'),
            'buyer_id': self.buyer_user_data['buyer_id']
        }
        # self.do_service(service_path, method_name, params)
        res = self.do_service('order.service.address.order_address_service', 'create_order_address', params=params)

        # if res['code'] == 0 and not params['addr_no']:
        #     buyer_params = {
        #         'city_no': self.params('city_no') if self.params('city_no') else 0,
        #         'district': self.params('district'),
        #         'street_addr': self.params('receiver_address'),
        #         'name': self.params('receiver_name'),
        #         'mobile_no': self.params('receiver_mobile'),
        #         'scen_type': self.buyer_user_data['scen_type'],
        #         'scen_id': self.buyer_user_data['scen_id'],
        #         'buyer_id': self.buyer_user_data['buyer_id']
        #     }
        #     redis = self.redis.get_conn()
        #     buyer_params['addr_no'] = redis.incr(self.cache_key_predix.BUYER_ADDR_NO)
        #     # self.do_service(service_path, method_name, params)
        #     self.do_service('buyer.service.address.buyer_address_service', 'create_buyer_addr', params=buyer_params)

        self.out(res)
