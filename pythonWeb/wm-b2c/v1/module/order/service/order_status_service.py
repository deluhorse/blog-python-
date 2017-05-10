# -*- coding:utf-8 -*-

"""
订单状态service
@author: onlyfu
@time: 4/27/2017
"""
from base.service import ServiceBase


class Service(ServiceBase):

    order_model = None

    def __init__(self):
        self.order_model = self.import_model('order.model.order_model')

    def check_order_status(self, params):
        """
        查询指定订单状态的订单是否存在
        :param order_id: 
        :param order_status: 
        :return: 
        """
        if self.order_model.query_order_count(params):
            return True
        else:
            return False
