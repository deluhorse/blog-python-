# -*- coding:utf-8 -*-

"""
图片model
@author: onlyfu
@time: 4/26/2017
"""
from source.model import ModelBase


class Model(ModelBase):
    def get_many(self, img_id_list):
        """
        获取多条图片记录
        :param img_id_list: 图片ID，多个用,号分隔
        :return: 
        """
        # 请求字段
        fields = []
        # 请求的值
        value_list = []

        condition = [" img_id in ("]
        in_list = []
        for item in img_id_list:
            in_list.append("%s")
            value_list.append(item)

        condition.append(','.join(in_list))
        condition.append(")")
        condition = ''.join(condition)

        return self.find('tbl_um_images',
                         {self.sql_constants.FIELDS: fields,
                          self.sql_constants.CONDITION: condition},
                         tuple(value_list),
                         self.sql_constants.LIST)
