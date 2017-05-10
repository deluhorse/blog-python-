# -*- coding:utf-8 -*-

"""
当前售卖商品
@author: onlyfu
@time: 5/3/2017
"""
from base.base import Base


class Controller(Base):
    def initialize(self):
        Base.initialize(self)

    def index(self):

        id = self.properties.get('sale', 'GOODS_ID')
        params = {
            'id': id
        }
        # self.do_service(service_path, method_name, params)
        result = self.do_service('goods.service.detail', 'detail', params=params)
        self.out(result)
