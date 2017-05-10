# -*- coding:utf-8 -*-

"""
@author: delu
@file: query.py
@time: 17/4/20 下午5:03
查询店铺详情
"""
from base.base import Base


class Controller(Base):

    user_type = ('seller',)

    def initialize(self):
        Base.initialize(self)

    def index(self):
        # self.do_service(service_path, method_name, params)

        params = {
            'shop_id': self.redis.incr(self.cache_key_predix.SHOP_ID),
            'admin_id': self.user_data['account_id'],
            'shop_name': self.params('shop_name'),
            'logo_url': self.params('logo_url')
        }

        res = self.do_service('shop.shop_service', 'create', params=params)