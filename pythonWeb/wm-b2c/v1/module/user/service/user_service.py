# -*- coding:utf-8 -*-

"""
@author: delu
@file: user_service.py
@time: 17/4/13 下午3:13
"""
from v1.base.service import ServiceBase


class Service(ServiceBase):
    """
    user_service
    """

    user_model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        self.user_model = self.import_model('user.model.user_model')

    def create(self, params):
        """
        注册管理员
        :param params: 
        :return: 
        """
        if 'password' not in params or not params['password'] \
                or 'check_password' not in params or not params['check_password'] \
                or 'account' not in params or not params['account']\
                or 'vertify_code' not in params or not params['vertify_code']:
            # 必要参数非空
            return self._e('ADMIN_PARAMS_NOT_EXITS')
        # 确认密码和密码不匹配
        if cmp(params['password'], params['check_password']) != 0:
            return self._e('PASSWORD_NOT_MATCH')
        # 账号已存在
        admin_nums = self.user_model.count_user_account(params)
        if admin_nums > 0:
            return self._e('ACCOUNT_EXIST')
        salt = self.salt()
        password = self.md5(self.md5(params['password']) + salt)

        params['password'] = password
        params['salt'] = salt

        res = self.user_model.create(params)

        if res is None:
            return self._e('SQL_EXECUTE_ERROR')
        else:
            return self._e('SUCCESS')

    def query_user(self, params):
        """
        查询管理员
        :param params: 
        :return: 
        """
        data = self.user_model.query_user_single(params)

        if data is None:
            return self._e('SQL_EXECUTE_ERROR')
        else:
            result = self._e('SUCCESS')
            result['data'] = data
            return result

    def login(self, params):
        """
        管理员登录
        :param params: 
        :return: 
        """

        # 查询账户信息
        user_account = self.user_model.query_user_account_single(params)
        if user_account is None:
            return self._e('ACCOUNT_NOT_FIND')

        if cmp(self.md5(self.md5(params['password']) + user_account['salt']), user_account['password']) == 0:

            # 登录成功
            # 生成cookie和服务端token
            result = self._e('SUCCESS')
            result['data'] = user_account
            return result

        else:
            return self._e('ERROR_PASSWORD')

    def update(self, params):
        """
        更新管理员信息
        :param params: 
        :return: 
        """
        res = self.user_model.update_user(params)

        if res is None:
            return self._e('SQL_EXECUTE_ERROR')
        else:
            return self._e('SUCCESS')
