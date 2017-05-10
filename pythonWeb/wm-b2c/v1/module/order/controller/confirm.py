# -*- coding:utf-8 -*-

"""
@author: delu
@file: confirm.py
@time: 17/5/9 下午6:05
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
        params['shop_id'] = self.buyer_user_data['shop_id']

        # self.do_service(service_path, method_name, params)
        res = self.do_service('order.service.order_confirm_service', 'get_order_confirm', params=params)
        self.out(res)
