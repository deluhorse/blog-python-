# -*- coding:utf-8 -*-

"""
@author: delu
@file: quit.py
@time: 17/4/24 上午11:46
"""
from base.base import Base


class Controller(Base):
    auth = (('seller',), 'post')

    def initialize(self):
        Base.initialize(self)

    def index(self):
        params = {
            'shop_id': self.user_data['shop_id'],
            'admin_id': self.user_data['admin_id']
        }
        # self.do_service(service_path, method_name, params)
        res = self.do_service('shop.service.shop_service', 'quit_shop', params=params)

        if res['code'] == 0:
            # 更新token缓存
            self.quit_shop()
        self.out(res)
