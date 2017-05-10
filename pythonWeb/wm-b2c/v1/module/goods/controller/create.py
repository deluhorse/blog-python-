# -*- coding:utf-8 -*-

"""
创建商品控制器
@author onlyfu
@file create.py
@time 17/04/25
"""

from base.base import Base


class Controller(Base):

    goods_service = None
    auth = (('admin',), 'post')

    def initialize(self):
        Base.initialize(self)

    def index(self):

        # 获取参数
        params = self.params()
        params['admin_id'] = self.user_data['admin_id']
        result = self.do_service('goods.service.goods_service', 'create', params=params)

        self.out(result)
