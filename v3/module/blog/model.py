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
        condition = ' is_delete = 0 '
        value_list = []
        if 'user_id' in params and params['user_id']:
            condition += ' and user_id = %s '
            value_list.append(params['user_id'])
        if 'blog_id' in params and params['blog_id']:
            condition += ' and blog_id = %s '
            value_list.append(params['blog_id'])
        if 'is_open' in params:
            condition += ' and is_open = %s '
            value_list.append(params['is_open'])
        order = ' create_time DESC '
        result = yield self.find('tbl_um_blog', {self.sql_constants.CONDITION: condition,
                                                 self.sql_constants.ORDER: order},
                                 tuple(value_list),
                                 self.sql_constants.LIST)
        raise self._gr(result)

    @tornado.gen.coroutine
    def query_blog_single(self, params):
        """
        查询单条博文记录
        :param params: 
        :return: 
        """
        condition = ' blog_id = %s and is_delete = 0 '
        value_list = [params['blog_id']]

        if 'user_id' in params and params['user_id']:
            condition += ' and user_id = %s '
            value_list.append(params['user_id'])

        result = yield self.find('tbl_um_blog', {self.sql_constants.CONDITION: condition}, tuple(value_list))

        raise self._gr(result)

    @tornado.gen.coroutine
    def query_blog_page(self, params):
        """
        分页查询博文
        :param params: 
        :return: 
        """
        condition = ' 1 = 1 and is_delete = 0 '
        value_list = []

        if 'user_id' in params and params['user_id']:
            condition += ' and user_id = %s '
            value_list.append(params['user_id'])
        if 'blog_id' in params and params['blog_id']:
            condition += ' and blog_id = %s '
            value_list.append(params['blog_id'])
        if 'is_open' in params:
            condition += ' and is_open = %s '
            value_list.append(params['is_open'])

        if 'page_index' not in params or 'page_size' not in params:
            params['page_index'] = 1
            params['page_size'] = 15

        limit = [params['page_index'], params['page_size']]
        order = 'create_time desc '
        result = yield self.page_find(
            'tbl_um_blog',
            {
                self.sql_constants.CONDITION: condition,
                self.sql_constants.ORDER: order,
                self.sql_constants.LIMIT: limit
            },
            tuple(value_list)
        )
        raise self._gr(result)

    @tornado.gen.coroutine
    def create_blog(self, params):
        """
        创建博文
        :param params: 
        :return: 
        """
        key = 'user_id, title, content'
        value_tuple = (params['user_id'], params['title'], params['content'])
        result = yield self.insert('tbl_um_blog', {self.sql_constants.KEY: key}, value_tuple)
        raise self._gr(result)

    @tornado.gen.coroutine
    def update_blog(self, params):
        """
        更新博文
        :param params: 
        :return: 
        """
        fields = [
            'title=%s',
            'content=%s'
        ]
        condition = ' blog_id = %s and user_id = %s '
        value_tuple = (params['title'], params['content'], params['blog_id'], params['user_id'])
        result = yield self.update(
            'tbl_um_blog',
            {
                self.sql_constants.FIELDS: fields,
                self.sql_constants.CONDITION: condition
            },
            value_tuple
        )
        raise self._gr(result)

    @tornado.gen.coroutine
    def delete_blog(self, params):
        """
        删除博文
        :param params: 
        :return: 
        """
        fields = [
            'is_delete=1'
        ]
        condition = ' blog_id = %s and user_id = %s '
        value_tuple = (params['blog_id'], params['user_id'])
        result = yield self.update(
            'tbl_um_blog',
            {
                self.sql_constants.FIELDS: fields,
                self.sql_constants.CONDITION: condition
            },
            value_tuple
        )
        raise self._gr(result)
