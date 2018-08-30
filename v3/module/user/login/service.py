# -*- coding:utf-8 -*-

"""
@author: delu
@file: service.py
@time: 18/5/7 20:32
"""
from base.service import ServiceBase
import tornado.gen


class Service(ServiceBase):
    """
    service
    """

    @tornado.gen.coroutine
    def login(self, params={}):
        if self.common_utils.is_empty(['user_name', 'password'], params):
            raise self._gre('PARAMS_NOT_EXIST')
        # 根据user_name查询账户信息
        account_result = yield self.do_model('user.account.model', 'query_account', params)
        if not account_result:
            raise self._gre('ACCOUNT_NOT_FOUND')
        if account_result['password'] != params['password']:
            raise self._gre('PASSWORD_ERROR')
        # 查询用户基本信息
        user_result = yield self.do_service('user.service', 'query_user', account_result)
        if user_result['code'] != 0:
            raise self._gr(user_result)
        account_result['user_info'] = user_result['data']
        raise self._grs(account_result)
