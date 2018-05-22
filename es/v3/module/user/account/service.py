# -*- coding:utf-8 -*-

"""
@author: delu
@file: service.py
@time: 18/5/14 20:55
"""
from base.service import ServiceBase
import tornado.gen


class Service(ServiceBase):
    """
    service
    """

    @tornado.gen.coroutine
    def query_account(self, params={}):
        """
        查询账号信息
        :param params: 
        :return: 
        """
        result = yield self.do_model('user.account.model', 'query_account', params)
        if result is False:
            raise self._gre('SQL_EXECUTE_ERROR')
        raise self._grs(result)
