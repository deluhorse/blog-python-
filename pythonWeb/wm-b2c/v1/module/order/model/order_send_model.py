# -*- coding:utf-8 -*-

"""
@author: delu
@file: order_send_model.py
@time: 17/5/5 下午2:19
"""

from source.model import ModelBase


class Model(ModelBase):
    def create_send(self, params):
        """
        创建发货记录并更改订单状态
        :param params: 
        :return: 
        """
        sql_list = []

        # 发货key
        send_key = 'order_id, logiscomp_id, tracking_id, remark'
        # 发货的val
        send_val = '%s, %s, %s, %s'
        # 发货的value
        send_value_tuple = (params['order_id'], params['logiscomp_id'], params['tracking_id'], params['remark'])

        sql_list.append({self.sql_constants.SQL_TYPE: self.sql_constants.INSERT,
                         self.sql_constants.TABLE_NAME: 'tbl_om_ordersend',
                         self.sql_constants.DICT_DATA: {self.sql_constants.KEY: send_key,
                                                        self.sql_constants.VAL: send_val},
                         self.sql_constants.VALUE_TUPLE: send_value_tuple})

        # 修改订单状态为已发货
        fields = ['order_status = 3']
        condition = ' order_id = %s '
        value_tuple = (params['order_id'],)

        sql_list.append({self.sql_constants.SQL_TYPE: self.sql_constants.UPDATE,
                         self.sql_constants.TABLE_NAME: 'tbl_om_order',
                         self.sql_constants.DICT_DATA: {self.sql_constants.FIELDS: fields,
                                                        self.sql_constants.CONDITION: condition},
                         self.sql_constants.VALUE_TUPLE: value_tuple})
        return self.do_sqls(sql_list)

    def create_receive(self, params):
        """
        创建收货记录
        :param params: 
        :return: 
        """
        sql_list = []
        # 创建订单收货记录
        receive_fields = ['receive_flag = 1', 'receive_time = now()']
        receive_condition = ' order_id = %s '
        receive_value_tuple = (params['order_id'],)

        sql_list.append({self.sql_constants.SQL_TYPE: self.sql_constants.UPDATE,
                         self.sql_constants.TABLE_NAME: 'tbl_om_ordersend',
                         self.sql_constants.DICT_DATA: {self.sql_constants.FIELDS: receive_fields,
                                                        self.sql_constants.CONDITION: receive_condition},
                         self.sql_constants.VALUE_TUPLE: receive_value_tuple})

        # 修改订单状态为已收货
        fields = ['order_status = %s']
        condition = ' order_id = %s '
        value_tuple = (params['order_status'], params['order_id'])

        sql_list.append({self.sql_constants.SQL_TYPE: self.sql_constants.UPDATE,
                         self.sql_constants.TABLE_NAME: 'tbl_om_order',
                         self.sql_constants.DICT_DATA: {self.sql_constants.FIELDS: fields,
                                                        self.sql_constants.CONDITION: condition},
                         self.sql_constants.VALUE_TUPLE: value_tuple})
        return self.do_sqls(sql_list)
