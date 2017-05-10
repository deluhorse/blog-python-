# -*- coding:utf-8 -*-

"""
@author: delu
@file: cfg_user_model.py
@time: 17/5/8 下午1:07
"""

from source.model import ModelBase


class Model(ModelBase):
    def get_one(self, admin_id='0'):
        """
        查询管理员配置
        """
        # 请求范围
        fields = ['cfg_content']
        # 请求条件
        condition = ' admin_id = %s '
        # 请求的value
        value_tuple = (admin_id,)
        return self.find('tbl_cfg_admin', {self.sql_constants.FIELDS: fields,
                                           self.sql_constants.CONDITION: condition}, value_tuple)
