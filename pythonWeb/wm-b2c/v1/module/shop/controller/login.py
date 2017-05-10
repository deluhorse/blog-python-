# -*- coding:utf-8 -*-

"""
@author: delu
@file: login.py
@time: 17/4/20 下午6:23
登录店铺
"""
from base.base import Base


class Controller(Base):
    auth = (('admin',), 'post')

    def initialize(self):
        Base.initialize(self)

    def index(self):
        params = {
            'shop_id': self.params('shop_id'),
            'admin_id': self.user_data['admin_id']
        }
        # self.do_service(service_path, method_name, params)
        res = self.do_service('shop.service.shop_service', 'login_shop', params=params)

        if res['code'] == 0:
            self.update_cookie_and_token(params)

        self.out(res)
