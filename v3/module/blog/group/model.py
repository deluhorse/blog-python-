# -*- coding:utf-8 -*-

"""
@author: delu
@file: model.py
@time: 18/9/6 11:50
"""

from source.async_model import AsyncModelBase
import tornado.gen


class Model(AsyncModelBase):
    @tornado.gen.coroutine
    def create_group(self, params):
        """
        创建分组
        """
        key = 'parent_group_id, group_name, user_id, height'
        value_tuple = (params['parent_group_id'], params['group_name'], params['user_id'], params['height'])
        result = yield self.insert('tbl_blog_group', {self.sql_constants.KEY: key}, value_tuple)

        raise self._gr(result)

    @tornado.gen.coroutine
    def update_group(self, params):
        """
        更新分组名称和父分组
        :param params: 
        :return: 
        """
        fields = [
            'group_id=%s'
        ]

        value_list = [params['group_id']]

        condition = ' group_id = %s and user_id = %s  '

        if 'group_name' in params and params['group_name']:

            fields.append('group_name=%s')
            value_list.append(params['group_name'])

        if 'parent_group_id' in params and params['parent_group_id']:

            fields.append('parent_group_id=%s')
            value_list.append(params['parent_group_id'])

        value_list.extend([params['group_id'], params['user_id']])

        result = yield self.update(
            'tbl_blog_group',
            {
                self.sql_constants.FIELDS: fields,
                self.sql_constants.CONDITION: condition
            },
            tuple(value_list)
        )

        raise self._gr(result)

    @tornado.gen.coroutine
    def query_group_single(self, params):
        """
        查询单个分组
        :param params: 
        :return: 
        """
        condition = ' group_id = %s '
        value_list = [params['group_id']]

        result = yield self.find('tbl_blog_group', {self.sql_constants.CONDITION: condition}, tuple(value_list))

        raise self._gr(result)

    @tornado.gen.coroutine
    def query_group_list(self, params):
        """
        查询分组列表
        :param params: 
        :return: 
        """
        condition = ' 1 = 1 '
        value_list = []

        if 'group_id_list' in params and params['group_id_list']:

            condition += ' and group_id ' + self.build_in(len(params['group_id_list']))
            value_list.extend(params['group_id_list'])

        if 'user_id' in params and params['user_id']:

            condition += ' and user_id = %s '
            value_list.append(params['user_id'])

        result = yield self.find('tbl_blog_group', {self.sql_constants.CONDITION: condition},
                                 tuple(value_list), self.sql_constants.LIST)

        raise self._gr(result)

    @tornado.gen.coroutine
    def delete_group(self, params):
        """
        批量删除分组
        :param params: 
        :return: 
        """
        condition = 'user_id = %s and group_id ' + self.build_in(len(params['group_id_list']))
        value_list = [params['user_id']]
        value_list.extend(params['group_id_list'])

        result = yield self.delete('tbl_blog_group', {self.sql_constants.CONDITION: condition}, tuple(value_list))

        raise self._gr(result)
