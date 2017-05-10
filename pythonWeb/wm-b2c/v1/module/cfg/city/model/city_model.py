# -*- coding:utf-8 -*-

"""
@author: delu
@file: city_model.py
@time: 17/5/10 下午3:00
"""

from source.model import ModelBase


class Model(ModelBase):
    def query_city_list(self, city_no_list):
        """
        查询城市列表
        :param city_no_list: 
        :return: 
        """
        # 查询范围
        fields = []
        # 查询条件
        condition = ' city_no ' + self.build_in(len(city_no_list))
        # 查询的值
        value_tuple = tuple(city_no_list)

        return self.find('tbl_cfg_citydef', {self.sql_constants.FIELDS: fields,
                                             self.sql_constants.CONDITION: condition},
                         value_tuple,
                         self.sql_constants.LIST)
