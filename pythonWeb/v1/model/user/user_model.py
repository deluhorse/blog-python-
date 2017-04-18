# -*- coding:utf-8 -*-

"""
@author: delu
@file: user_model.py
@time: 17/4/13 下午3:22
"""

from source.model import ModelBase


class Model(ModelBase):

    def get_many(self, params):
        # 请求字段
        fields = []
        # 请求条件
        condition = ' 1 = 1 '

        if 'account_id' in params:
            condition += " and account_id = '%s' " % params['account_id']

        if 'uid' in params:
            condition += " and account.uid = '%s' " % params['uid']

        if 'account' in params:
            condition += " and account = '%s' " % params['account']

        # 表链接
        join = [
            {'table_name': 'users AS user1', 'join_condition': 'account.uid = user1.uid'},
            {'table_name': 'users AS user2', 'join_condition': 'account.uid = user2.uid'}
        ]

        limit = ['0', '10']

        data_list = self.paginate('user_account AS account', {'fields': fields, 'condition': condition, 'join': join,
                                                              'limit': limit})

        return data_list

    def create(self, params):

        """
        创建
        :param params: 
        :return: 
        """
        key = 'account_id, uid, account, password, salt, account_type, status'
        val = "'%s','%s','%s','%s','%s','%s','%s'" % (params['account_id'], params['uid'], params['account'],
                                                      params['password'], params['salt'], params['account_type'],
                                                      params['status'])
        res = self.insert('user_account', {'key': key, 'val': val})

    def update(self, params):

        """
        更新
        :param params: 
        :return: 
        """

        # self.update(params)

    def delete(self, params):

        """
        删除
        :param params: 
        :return: 
        """
        # self.delete(params)
