# -*- coding:utf-8 -*-

"""
@author: delu
@file: buyer_model.py
@time: 17/4/24 下午4:03
"""

from source.model import ModelBase


class Model(ModelBase):
    def query_buyer_count(self, params):
        """
        查询买家数量
        """
        # 查询条件
        condition = ' 1 = 1 '
        # 查询的值
        value_list = []

        if 'mobile_no' in params and params['mobile_no']:
            condition += ' and mobile_no = %s '
            value_list.append(params['mobile_no'])
        if 'buyer_id' in params and params['buyer_id']:
            condition += ' and buyer_id = %s '
            value_list.append(params['buyer_id'])

        return self.get_rows('tbl_um_buyer', {self.sql_constants.CONDITION: condition}, tuple(value_list))

    def query_buyer(self, params):
        """
        查询买家基本信息
        :param params: 
        :return: 
        """
        # 查询字段
        fields = []
        # 查询条件
        condition = ' 1 = 1 '
        # 查询的值
        value_list = []

        if 'buyer_id' in params and params['buyer_id']:
            condition += ' and buyer_id = %s '
            value_list.append(params['buyer_id'])
        if 'mobile_no' in params and params['mobile_no']:
            condition += ' and mobile_no = %s '
            value_list.append(params['mobile_no'])
        return self.find('tbl_um_buyer', {self.sql_constants.FIELDS: fields,
                                          self.sql_constants.CONDITION: condition}, tuple(value_list))

    def create_buyer(self, params):
        """
        创建买家
        :param params: 
        :return: 
        """
        key = 'scen_type, scen_id, shop_id, buyer_id, mobile_no'
        val = '%s, %s, %s, %s, %s'
        value_tuple = (params['scen_type'], params['scen_id'], params['shop_id'], params['buyer_id'], params['mobile_no'])

        return self.insert('tbl_um_buyer', {self.sql_constants.KEY: key,
                                            self.sql_constants.VAL: val}, value_tuple)
