# -*- coding:utf-8 -*-

"""
@author: delu
@file: order_send_service.py
@time: 17/5/5 下午2:36
"""
from base.service import ServiceBase


class Service(ServiceBase):
    """
    order_send_service
    """

    order_model = None
    order_send_model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        self.order_model = self.import_model('order.model.order_model')
        self.order_send_model = self.import_model('order.model.order_send_model')

    def create_send(self, params):
        """
        创建订单发货记录
        :param params: 
        :return: 
        """
        if self.common_utils(['order_id', 'logiscomp_id', 'tracking_id'], params):
            # 必要参数校验
            return self._e('ORDER_SEND_PARAMS_NOT_EXIST')
        if not self.do_service('order.service.order_base_service', 'check_order', params):
            # 业务权限校验
            return self._e('ORDER_SHOP_NOT_PERMISSION')
        params['order_status'] = self.constants.ORDER_PAY_SUCCESS
        if not self.do_service('order.service.order_status_service', 'check_order_status', params):
            # 业务权限校验
            return self._e('ORDER_STATUS_CHANGE_NOT_PERMISSION')

        result = self.order_send_model.create_send(params)
        if result is None:
            return self._e('SQL_EXECUTE_ERROR')
        else:
            return self._e('SUCCESS')

    def create_receive(self, params):
        """
        创建订单收货记录
        :param params: 
        :return: 
        """
        if self.common_utils(['order_id'], params):
            # 必要参数校验
            return self._e('ORDER_RECEIVE_PARAMS_NOT_EXIST')
        if not self.do_service('order.service.order_base_service', 'check_order', params):
            # 业务权限校验
            return self._e('ORDER_BUYER_NOT_PERMISSION')
        params['order_status'] = self.constants.ORDER_SEND
        if not self.do_service('order.service.order_status_service', 'check_order_status', params):
            # 业务权限校验
            return self._e('ORDER_STATUS_CHANGE_NOT_PERMISSION')

        result = self.order_send_model.create_receive(params)
        if result is None:
            return self._e('SQL_EXECUTE_ERROR')
        else:
            return self._e('SUCCESS')
