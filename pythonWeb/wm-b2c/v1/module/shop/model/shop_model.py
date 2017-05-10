# -*- coding:utf-8 -*-

"""
@author: delu
@file: shop_model.py
@time: 17/4/20 下午5:10
"""

from source.model import ModelBase


class Model(ModelBase):
    def create_shop(self, params):
        """
        创建店铺
        """
        key = 'shop_id, admin_id, shop_name, logo_url'
        val = '%s, %s, %s, %s'
        value_tuple = (params['shop_id'], params['admin_id'], params['shop_name'], params['logo_url'])

        return self.insert('tbl_um_shop', {self.sql_constants.KEY: key,
                                           self.sql_constants.VAL: val}, value_tuple)

    def update_shop(self, params):
        """
        更新店铺
        :param params: 
        :return: 
        """
        fields = ['shop_name = %s', 'logo = %s']
        condition = ' shop_id = %s'
        values_tuple = (params['shop_name'], params['logo'], params['shop_id'])

        return self.update('shops', {self.sql_constants.FIELDS: fields,
                                     self.sql_constants.CONDITION: condition}, values_tuple)

    def query_shop_count(self, params):
        """
        查询店铺数量
        :param params: 
        :return: 
        """
        condition = ' 1 = 1 '
        value_list = []

        if 'shop_id' in params:
            condition += 'and shop_id = %s'
            value_list.append(params['shop_id'])
        if 'admin_id' in params:
            condition += 'and admin_id = %s'
            value_list.append(params['admin_id'])

        return self.get_rows('tbl_um_shop', {self.sql_constants.CONDITION: condition}, tuple(value_list))

    def query_shop(self, params):
        """
        查询店铺列表
        :param params: 
        :return: 
        """
        # 查询范围
        fields = []
        # 查询条件
        condition = ' 1 = 1 '
        # 查询的值
        value_list = []
        if 'shop_id' in params and params['shop_id']:
            condition += ' and shop_id = %s '
            value_list.append(params['shop_id'])
        if 'admin_id' in params and params['admin_id']:
            condition += ' and admin_id = %s '
            value_list.append(params['admin_id'])
        return self.find('tbl_um_shop', {self.sql_constants.FIELDS: fields,
                                         self.sql_constants.CONDITION: condition}, tuple(value_list))
