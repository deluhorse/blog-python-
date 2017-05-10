# -*- coding:utf-8 -*-

"""
@author: delu
@file: create.py
@time: 17/4/20 下午5:02
创建店铺
"""
from base.base import Base


class Controller(Base):

    user_type = ('admin',)

    def initialize(self):
        Base.initialize(self)

    def index(self):
        redis = self.redis.get_conn()
        params = {
            'admin_id': self.user_data['admin_id'],
            'shop_name': self.params('shop_name'),
            'shop_id': redis.incr(self.cache_key_predix.SHOP_ID),
            'logo_url': self.params('logo_url')
        }
        # self.do_service(service_path, method_name, params)
        res = self.do_service('shop.service.shop_service', 'create_shop', params=params)

        self.out(res)
