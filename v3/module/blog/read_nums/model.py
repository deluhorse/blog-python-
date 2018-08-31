# -*- coding:utf-8 -*-

"""
@author: delu
@file: model.py
@time: 18/8/31 14:08
"""

from source.async_model import AsyncModelBase
import tornado.gen


class Model(AsyncModelBase):
    @tornado.gen.coroutine
    def update_read_nums(self, params):
        """
        更新阅读人数
        """
        fields = [
            'read_nums = read_nums + 1'
        ]
        condition = ' blog_id = %s '
        value_tuple = (params['blog_id'],)
        result = yield self.update(
            'tbl_um_blog',
            {
                self.sql_constants.FIELDS: fields,
                self.sql_constants.CONDITION: condition
            },
            value_tuple
        )

        raise self._gr(result)
