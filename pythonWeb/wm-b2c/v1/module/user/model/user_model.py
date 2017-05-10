# -*- coding:utf-8 -*-

"""
@author: delu
@file: user_model.py
@time: 17/4/13 下午3:22
"""

from source.model import ModelBase


class Model(ModelBase):
    def count_user_account(self, params):
        """
        查询管理员账号数量
        :param params: 
        :return: 
        """
        # 请求条件
        condition = ' 1 = 1 '
        # 请求的值
        value_list = []

        if 'account' in params and params['account_id']:
            condition += ' and account = %s '
            value_list.append(params['account'])
        return self.get_rows('tbl_um_adminaccount', {self.sql_constants.CONDITION: condition}, tuple(value_list))

    def query_user_account_single(self, params):
        """
        查询管理员账号信息
        :param params: 
        :return: 
        """
        # 请求字段
        fields = []
        # 请求条件
        condition = ' 1 = 1 '
        # 请求的值
        value_list = []

        if 'account_id' in params:
            condition += " and account_id = %s "
            value_list.append(params['account_id'])
        if 'account' in params:
            condition += " and account = %s "
            value_list.append(params['account'])

        return self.find('tbl_um_adminaccount', {self.sql_constants.FIELDS: fields,
                                                 self.sql_constants.CONDITION: condition}, tuple(value_list))

    def query_user_single(self, params):
        """
        查询管理员基本信息
        :param params: 
        :return: 
        """
        # 请求字段
        fields = []
        # 查询条件
        condition = ' 1 = 1 '
        # 查询的值
        value_list = []

        if 'admin_id' in params:
            condition += ' and admin_id = %s '
            value_list.append(params['admin_id'])
        return self.find('tbl_um_admin', {self.sql_constants.FIELDS: fields,
                                          self.sql_constants.CONDITION: condition}, tuple(value_list))

    def get_many(self, params):
        # 请求字段
        fields = []
        # 请求条件
        condition = ' 1 = 1 '
        # 请求的值
        value_list = []

        if 'account_id' in params:
            condition += " and account_id = %s "
            value_list.append(params['account_id'])
        if 'uid' in params:
            condition += " and account.uid = %s "
            value_list.append(params['uid'])
        if 'account' in params:
            condition += " and account = %s "
            value_list.append(params['account'])

        # 表链接
        join = [
            {self.sql_constants.TABLE_NAME: 'users AS user1',
             self.sql_constants.JOIN_CONDITION: 'account.uid = user1.uid'},
            {self.sql_constants.TABLE_NAME: 'users AS user2',
             self.sql_constants.JOIN_CONDITION: 'account.uid = user2.uid'}
        ]
        # 分页
        limit = ['0', '10']

        data_list = self.page_find('user_account as account', {self.sql_constants.FIELDS: fields,
                                                               self.sql_constants.CONDITION: condition,
                                                               self.sql_constants.JOIN: join,
                                                               self.sql_constants.LIMIT: limit}, tuple(value_list))
        return data_list

    def create(self, params):

        """
        创建
        :param params: 
        :return: 
        """
        sql_list = []
        account_key = 'account_id, admin_id, account, password, salt'
        account_val = '%s,%s,%s,%s,%s'
        account_value_tuple = (params['account_id'], params['admin_id'], params['account'], params['password'],
                               params['salt'])
        sql_list.append({self.sql_constants.SQL_TYPE: self.sql_constants.INSERT,
                         self.sql_constants.TABLE_NAME: 'tbl_um_adminaccount',
                         self.sql_constants.DICT_DATA: {self.sql_constants.KEY: account_key,
                                                        self.sql_constants.VAL: account_val},
                         self.sql_constants.VALUE_TUPLE: account_value_tuple})

        user_key = 'admin_id'
        user_val = '%s'
        user_value_tuple = (params['admin_id'],)
        sql_list.append({'sql_type': self.sql_constants.INSERT,
                         'table_name': 'tbl_um_admin',
                         'dict_data': {'key': user_key, 'val': user_val},
                         'value_tuple': user_value_tuple})
        return self.do_sqls(sql_list)

    def update_user(self, params):

        """
        更新
        :param params: 
        :return: 
        """
        # 需要更新的区域
        fields = []
        # 查询条件
        condition = ''
        value_list = []

        if 'nick_name' in params:
            fields.append('nick_name = %s ')
            value_list.append(params['nick_name'])
        if 'mobile_no' in params:
            fields.append(' mobile_no = %s ')
            value_list.append(params['mobile_no'])
        if 'qq_account' in params:
            fields.append(' qq_account = %s ')
            value_list.append(params['qq_account'])
        if 'email_address' in params:
            fields.append(' email_address = %s ')
            value_list.append(params['email_address'])

        condition += ' admin_id = %s'
        value_list.append(params['admin_id'])

        return self.update('tbl_um_admin', {self.sql_constants.FIELDS: fields,
                                            self.sql_constants.CONDITION: condition}, tuple(value_list))

    def delete(self, params):

        """
        删除
        :param params: 
        :return: 
        """
        # self.delete(params)
        pass
