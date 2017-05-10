# -*- coding:utf-8 -*-

"""
@author: delu
@file: user_shop_service.py
@time: 17/4/24 下午12:20
"""
from base.service import ServiceBase


class Service(ServiceBase):
    """
    user_shop_service
    """

    user_shop_model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        self.user_shop_model = self.import_model('user.model.shop.user_shop_model')

    def query_shop_list(self, params):
        """
        查询管理员店铺列表
        :return: 
        """

        shop_list = self.user_shop_model.query_shop_list(params)
        if shop_list is None:
            return self._e('SQL_EXECUTE_ERROR')
        else:
            result = self._e('SUCCESS')
            result['data'] = shop_list
            return result
