# -*- coding:utf-8 -*-

"""
@author: delu
@file: model.py
@time: 18/5/14 12:16
"""

from source.async_model import AsyncModelBase
import tornado.gen


class Model(AsyncModelBase):
    @tornado.gen.coroutine
    def query_blog(self, params):
        """
        查询博客记录
        """
        # 请求数据
        condition = ' 1=1 '
        value_list = []
        if 'user_id' in params and params['user_id']:
            condition += ' and user_id = %s '
            value_list.append(params['user_id'])
        if 'blog_id' in params and params['blog_id']:
            condition += ' and blog_id = %s '
            value_list.append(params['blog_id'])
        if 'is_open' in params and params['is_open']:
            condition += ' and is_open = %s '
            value_list.append(params['is_open'])
        order = ' create_time DESC '
        result = yield self.find('tbl_um_blog', {self.sql_constants.CONDITION: condition,
                                                 self.sql_constants.ORDER: order},
                                 tuple(value_list),
                                 self.sql_constants.LIST)
        raise self._gr(result)

    @tornado.gen.coroutine
    def create_blog(self, params):
        """
        创建博客记录
        :param params: 
        :return: 
        """
        key = 'user_id, title, content'
        value_tuple = (params['user_id'], params['title'], params['content'])
        result = yield self.insert('tbl_um_blog', {self.sql_constants.KEY: key},
                                   value_tuple)
        raise self._gr(result)
