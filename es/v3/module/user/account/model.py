# -*- coding:utf-8 -*-

"""
@author: delu
@file: model.py
@time: 18/5/14 20:55
"""

from source.async_model import AsyncModelBase
import tornado.gen


class Model(AsyncModelBase):
    @tornado.gen.coroutine
    def query_account(self, params):
        """
        查询账号信息
        """
        condition = ' 1=1 '
        value_list = []
        if 'user_name' in params and params['user_name']:
            condition += ' and user_name = %s '
            value_list.append(params['user_name'])
        result = yield self.find('tbl_um_account', {self.sql_constants.CONDITION: condition}, tuple(value_list))
        raise self._gr(result)
