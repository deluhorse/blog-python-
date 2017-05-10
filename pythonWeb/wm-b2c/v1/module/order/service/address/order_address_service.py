# -*- coding:utf-8 -*-

"""
@author: delu
@file: order_address_service.py
@time: 17/4/28 上午9:51
"""
from base.service import ServiceBase


class Service(ServiceBase):
    """
    order_address_service
    """

    order_address_model = None
    order_model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        self.order_address_model = self.import_model('order.model.address.order_address_model')
        self.order_model = self.import_model('order.model.order_model')

    def create_order_address(self, params):
        """
        创建订单地址
        :param params: 
        :return: 
        """
        if 'order_id' not in params or not params['order_id']:
            return self._e('ORDER_ADDRESS_CREATE_PARAMS_ERROR')
        # 查询订单数量，确认该订单属于当前买家
        if self.order_model.query_order_count(params) > 0:
            return self.order_address_model.update_order_address(params)
        else:
            return self._e('ORDER_BUYER_NOT_PERMISSION')

