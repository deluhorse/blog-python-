# -*- coding:utf-8 -*-

"""
@author: delu
@file: shop_service.py
@time: 17/4/20 下午5:08
"""
from base.service import ServiceBase


class Service(ServiceBase):
    """
    shop_service
    """

    shop_model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        self.shop_model = self.import_model('shop.model.shop_model')

    def create_shop(self, params):
        """
        创建店铺
        :param params: 
        :return: 
        """
        data = self.shop_model.create_shop(params)
        if data is None:
            return self._e('SQL_EXECUTE_ERROR')
        else:
            return self._e('SUCCESS')

    def login_shop(self, params):
        """
        登录店铺
        :param params: 
        :return: 
        """
        data = self.shop_model.query_shop(params)

        if data is None:
            return self._e('SQL_EXECUTE_ERROR')
        elif not data:
            return self._e('SHOP_NOT_PERMISSION')
        else:
            result = self._e('SUCCESS')
            result['data'] = data
            return result

    def quit_shop(self, params):
        """
        退出店铺
        :param params: 
        :return: 
        """
        row_count = self.shop_model.query_shop_count(params)

        if row_count is None:
            return self._e('SQL_EXECUTE_ERROR')
        elif row_count == 0:
            return self._e('SHOP_NOT_PERMISSION')
        else:
            return self._e('SUCCESS')
