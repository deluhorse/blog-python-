# -*- coding:utf-8 -*-

"""
@author: delu
@file: login.py
@time: 17/4/24 下午3:57
"""
from base.base import Base


class Controller(Base):
    def initialize(self):
        Base.initialize(self)

    def index(self):
        params = {
            'mobile_no': self.params('mobile_no'),
            'vertify_code': self.params('vertify_code'),
            'scen_type': self.params('scen_type'),
            'scen_id': self.params('scen_id'),
            'shop_id': self.params('shop_id')
        }
        params['scen_type'] = params['scen_type'] if params['scen_type'] else '3'
        params['scen_id'] = params['scen_id'] if params['scen_id'] else 'wap'
        res = self.do_service('buyer.service.buyer_service', 'login', params=params)

        if res['code'] == 0:
            # 登录成功, 写cookie和token
            result = self.create_cookie_and_token_for_buyer(res['data'])
            res['data'] = result['buyer_token']

        self.out(res)
