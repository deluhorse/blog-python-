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
    def query_user(self, params={}):
        """
        查询用户信息
        :param params: 
        :return: 
        """
        result = yield self.do_model('user.model', 'query_user', params)
        if not result:
            raise self._gre('USER_NOT_FOUND')
        raise self._grs(result)

    @tornado.gen.coroutine
    def create_user(self, params):
        """
        创建用户
        :param params: 
        密码暂时不做md5加密, 昵称为5位随机字符串
        用户id为5位随机字符串
        :return: 
        """
        if self.common_utils.is_empty(['user_name', 'password'], params):
            raise self._gre('PARAMS_NOT_EXIST')
        user_result = yield self.do_service('user.account.service', 'query_account', {'user_name': params['user_name']})
        if user_result['code'] != 0:
            raise self._gr(user_result)
        if user_result['data']:
            raise self._gre('ACCOUNT_REPEAT')
        params['nick_name'] = params.get('nick_name', self.salt(5))
        params['user_id'] = self.salt(5)
        result = yield self.do_model('user.model', 'create_user', params)
        if not result:
            raise self._gre('SQL_EXECUTE_ERROR')
        raise self._grs()
