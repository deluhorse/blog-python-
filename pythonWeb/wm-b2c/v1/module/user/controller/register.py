# -*- coding:utf-8 -*-

"""
@author: delu
@file: user.py
@time: 17/4/13 下午2:53
管理员注册
"""

from v1.base.base import Base


class Controller(Base):
    userService = None

    def initialize(self):
        Base.initialize(self)

    def index(self):
        """
        注册管理员
        :return: 
        """
        redis = self.redis.get_conn()
        params = {
            'vertify_code': self.params('vertify_code'),
            'account_id': redis.incr(self.cache_key_predix.ACCOUNT_ID),
            'admin_id': redis.incr(self.cache_key_predix.ADMIN_ID),
            'password': self.params('password'),
            'check_password': self.params('check_password'),
            'account': self.params('username')
        }

        res = self.do_service('user.service.user_service', 'create', params=params)
        self.out(res)
