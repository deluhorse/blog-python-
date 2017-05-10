# -*- coding:utf-8 -*-

"""
@author: delu
@file: order_query_service.py
@time: 17/4/27 上午9:06
"""
from base.service import ServiceBase


class Service(ServiceBase):
    """
    order_query_service
    """

    order_model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        self.order_model = self.import_model('order.model.order_model')

    def query_order(self, params):
        """
        查询订单
        :param params: 
        :return: 
        """
        result = self.order_model.query_order(params)
        if result:
            res = self._e('SUCCESS')
            res['data'] = result
            return res
        else:
            return self._e('SQL_EXECUTE_ERROR')
