# -*- coding:utf-8 -*-

"""
@author: delu
@file: user_shop_model.py
@time: 17/4/24 下午12:25
"""

from source.model import ModelBase


class Model(ModelBase):
    def query_shop_list(self, params):
        """
        """

        # 请求数据
        # self.find(tableName, queryType, data)
        fields = []
        condition = ' 1 = 1 '
        value_list = []

        if 'admin_id' in params:
            condition += ' and admin_id = %s '
            value_list.append(params['admin_id'])

        return self.find('tbl_um_shop',
                         {self.sql_constants.FIELDS: fields,
                          self.sql_constants.CONDITION: condition},
                         tuple(value_list),
                         self.sql_constants.LIST)
