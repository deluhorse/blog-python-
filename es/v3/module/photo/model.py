# -*- coding:utf-8 -*-

"""
@author: delu
@file: model.py
@time: 18/5/7 20:18
"""

from source.async_model import AsyncModelBase
import tornado.gen


class Model(AsyncModelBase):
    @tornado.gen.coroutine
    def create_photo(self, params):
        """
        创建图片库记录
        """
        key = 'user_id, host_type, img_key, nick_name'
        value_tuple = (params['user_id'], params['host'], params['key'], params.get('nick_name', '未命名'))
        result = yield self.insert('tbl_um_photo', {self.sql_constants.KEY: key}, value_tuple)
        raise self._gr(result)

    @tornado.gen.coroutine
    def query_photo_list(self, params):
        """
        查询图片列表
        :param params: 
        :return: 
        """
        condition = ' img_key is not null '
        value_list = []

        if 'user_id' in params and params['user_id']:
            condition += ' and user_id = %s '
            value_list.append(params['user_id'])
        result = yield self.find(
            'tbl_um_photo',
            {
                self.sql_constants.CONDITION: condition
            },
            tuple(value_list),
            self.sql_constants.LIST)
        raise self._gr(result)
