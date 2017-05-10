# -*- coding:utf-8 -*-

"""
@author: delu
@file: buyer_address_service.py
@time: 17/4/27 下午3:28
"""
from base.service import ServiceBase


class Service(ServiceBase):
    """
    buyer_address_service
    """

    buyer_address_model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        self.buyer_address_model = self.import_model('buyer.model.address.buyer_address_model')

    def create_buyer_addr(self, params):
        """
        创建买家收货地址
        :param params: 
        :return: 
        """
        result = self.buyer_address_model.create_address(params)

        if result:
            return result
        else:
            return self._e('SQL_EXECUTE_ERROR')

    def query_address_list(self, params):
        """
        查询买家地址列表
        :param params: 
        :return: 
        """
        result = self.buyer_address_model.query_address_list(params)

        if result:
            res = self._e('SUCCESS')
            res['data'] = result
            return res
        else:
            return self._e('SQL_EXECUTE_ERROR')

    def query_default_addr(self, params):
        """
        查询买家默认地址
        :param params: 
        :return: 
        """
        result = self.buyer_address_model.query_default_addr(params)

        if result:
            res = self._e('SUCCESS')
            res['data'] = result
            return res
        else:
            return self._e('SQL_EXECUTE_ERROR')

    def update_default_addr(self, params):
        """
        修改买家默认地址
        :param params: 
        :return: 
        """

        result = self.buyer_address_model.update_default_addr(params)

        if result:
            return result
        else:
            return self._e('SQL_EXECUTE_ERROR')
