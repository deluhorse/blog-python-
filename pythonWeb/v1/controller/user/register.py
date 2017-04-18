# -*- coding:utf-8 -*-

"""
@author: delu
@file: user.py
@time: 17/4/13 下午2:53
"""

from controller.base import Base


class Controller(Base):
    userService = None

    def initialize(self):
        Base.initialize(self)

    def index(self):
        """
        注册管理员
        :return: 
        """
        #params = eval(self.params('para'))

        params = {
            'vertify_code': '111',
            'password': '123456',
            'account': "18602337250",
            'account_type': 2,
            'status': 1
        }

        vertify_code = params['vertify_code']
        account_id = self.redis.incr(self.cache_key_predix.ACCOUNT_ID)
        uid = self.redis.incr(self.cache_key_predix.UID)
        password = params['password']
        account = params['account']

        params['account_id'] = account_id
        params['uid'] = uid

        res = self.do_service('user.user_service', 'create', params=params)

        if res == -1:
            self.out(1002, '注册失败')
        else:
            self.out(0, '成功')
