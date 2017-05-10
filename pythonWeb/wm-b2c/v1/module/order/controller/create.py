# -*- coding:utf-8 -*-

"""
@author: delu
@file: create.py
@time: 17/4/27 上午5:42
"""
from base.base import Base


class Controller(Base):

    auth = (('buyer',), 'post')

    def initialize(self):
        Base.initialize(self)

    def index(self):
        params = self.params()
        params['goods_list'] = self.json.loads(params['goods_list'] if 'goods_list' in params else '[]')
        params['receive'] = self.json.loads(params['receive'] if 'receive' in params else '{}')
        params['scen_type'] = self.buyer_user_data['scen_type']
        params['scen_id'] = self.buyer_user_data['scen_id']
        params['buyer_id'] = self.buyer_user_data['buyer_id']
        params['client_ip'] = self.request.remote_ip
        params['shop_id'] = self.buyer_user_data['shop_id']
        if 'receive' not in params or not params['receive']:
            params['receive'] = {}
            params['receive']['name'] = ''
            params['receive']['address'] = ''
            params['receive']['mobile_no'] = ''
            params['receive']['city_no'] = '0'

        # self.do_service(service_path, method_name, params)
        res = self.do_service('order.service.order_create_service', 'create_order', params=params)
        self.out(res)
