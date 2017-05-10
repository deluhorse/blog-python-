# -*- coding:utf-8 -*-

"""
查询商品详情
@author: onlyfu
@time: 4/26/2017
"""
from base.base import Base


class Controller(Base):

    goods_service = None
    auth = (None, 'get')

    def initialize(self):
        Base.initialize(self)

    def index(self):

        # 获取参数
        params = self.params()
        result = self.do_service('goods.service.detail', 'detail', params=params)
        # result = self.do_service('goods.goods_service', 'get_sku', params=params)
        self.out(result)
