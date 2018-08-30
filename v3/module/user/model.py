# -*- coding:utf-8 -*-

"""
@author: delu
@file: model.py
@time: 18/5/14 20:30
"""

from source.async_model import AsyncModelBase
import tornado.gen


class Model(AsyncModelBase):

    @tornado.gen.coroutine
    def create_user(self, params):
        """
        创建用户
        :param params: 
        :return: 
        """
        sql_list = []
        # 创建用户基本信息
        user_key = 'user_id, nick_name'
        user_tuple = (params['user_id'], params['nick_name'])
        sql_list.append({self.sql_constants.SQL_TYPE: self.sql_constants.INSERT,
                         self.sql_constants.TABLE_NAME: 'tbl_um_user',
                         self.sql_constants.DICT_DATA: {self.sql_constants.KEY: user_key},
                         self.sql_constants.VALUE_TUPLE: user_tuple})
        # 创建用户账户
        account_key = 'user_id, user_name, password'
        account_tuple = (params['user_id'], params['user_name'], params['password'])
        sql_list.append({self.sql_constants.SQL_TYPE: self.sql_constants.INSERT,
                         self.sql_constants.TABLE_NAME: 'tbl_um_account',
                         self.sql_constants.DICT_DATA: {self.sql_constants.KEY: account_key},
                         self.sql_constants.VALUE_TUPLE: account_tuple})
        result = yield self.do_sqls(sql_list)
        raise self._gr(result)

    @tornado.gen.coroutine
    def query_user(self, params):
        """
        查询用户信息
        """
        condition = ' 1=1 '
        value_list = []
        if 'user_id' in params and params['user_id']:
            condition += ' and user_id = %s '
            value_list.append(params['user_id'])
        if 'nick_name' in params and params['nick_name']:
            condition += ' and nick_name = %s '
            value_list.append(params['nick_name'])
        result = yield self.find('tbl_um_user', {self.sql_constants.CONDITION: condition}, tuple(value_list))
        raise self._gr(result)
