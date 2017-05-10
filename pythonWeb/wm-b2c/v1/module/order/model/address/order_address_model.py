# -*- coding:utf-8 -*-

"""
@author: delu
@file: order_address_model.py
@time: 17/4/28 上午9:57
"""

from source.model import ModelBase


class Model(ModelBase):
    def update_order_address(self, params):
        """
        更新订单地址
        :param params: 
        :return: 
        """
        # 更新范围
        fields = ['receiver = %s', 'receiver_phone = %s', 'receiver_addr = %s']
        # 查询条件
        condition = ' order_id = %s and buyer_id = %s '
        # 更新的值
        value_tuple = (params['receiver_name'], params['receiver_mobile'], params['receiver_address'],
                       params['order_id'], params['buyer_id'])

        return self.update('tbl_om_order', {self.sql_constants.FIELDS: fields,
                                            self.sql_constants.CONDITION: condition}, value_tuple)
