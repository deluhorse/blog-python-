# -*- coding:utf-8 -*-

"""
@author: delu
@file: query.py
@time: 17/4/20 下午5:03
管理员查询店铺列表
"""
from v1.base.base import Base


class Controller(Base):

    auth = (('admin',), 'get')

    def initialize(self):
        Base.initialize(self)

    def index(self):
        # self.do_service(service_path, method_name, params)

        params = {
            'admin_id': self.user_data['admin_id'],
        }

        res = self.do_service('user.service.shop.user_shop_service', 'query_shop_list', params=params)

        self.out(res)
